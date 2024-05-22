import numpy as np
import numpy.linalg as npl
import cv2
from skimage.transform import resize
from .common import to_gray

DEFAULT_SIGMA=3.5

def get_crop_region(mask, crop_mode, sigma):
    hw_ratio = mask.shape[0] / mask.shape[1]

    rows, cols = np.where(mask)

    if crop_mode == 'bbox':
        min_y, max_y = rows.min(), rows.max()
        min_x, max_x = cols.min(), cols.max()

        cx = (max_x + min_x)/2
        cy = (max_y + min_y)/2

        rx = max(abs(max_x - cx), abs(cx - min_x))
        ry = max(abs(max_y - cy), abs(cy - min_y))
    elif crop_mode == 'mean':
        cx = cols.mean()
        cy = rows.mean()

        rx = sigma*cols.std()
        ry = sigma*rows.std()

    if (rx * hw_ratio) <= ry:
        rx = (ry / hw_ratio)
    else:
        ry = rx * hw_ratio

    return (cx-rx, cx+rx, cy-ry, cy+ry)

class ForegroundCentralCrop:
    def __init__(self, mask, out_size, crop_mode='bbox', order=0, gap=0.1,
                 pad_kws={}, sigma=DEFAULT_SIGMA):
        assert mask.ndim == 2
        self.imh, self.imw = mask.shape[:2]
        self.out_size = out_size
        if 0 < gap < 1:
            gap = int(max(self.out_size)*gap)
        self.gap = gap
        self.mask = mask
        self.pad_l = max(self.imw, self.imh)
        self.order = order
        pad_kws.setdefault('mode', 'constant')
        self.pad_kws = pad_kws

        mask_ext = np.pad(mask, (self.pad_l, self.pad_l), **self.pad_kws)
        xs = get_crop_region(mask_ext, crop_mode=crop_mode, sigma=sigma)
        self.x0, self.x1, self.y0, self.y1 = [int(i) for i in xs]
        mask_ext[self.y0:self.y1, self.x0:self.x1] = 0
        self.is_unsafe_crop = mask_ext.any()

    def __call__(self, *imgs):
        cropped_imgs = []
        rois = []
        for img in imgs:
            assert img.shape[:2] == (self.imh, self.imw), f'img_shape {img.shape} != self.img_size ({self.imh} {self.imw})'
            gap, pad_l = self.gap, self.pad_l
            img_ext = np.pad(img, ((pad_l, pad_l), (pad_l, pad_l)), **self.pad_kws)

            cropped_img = img_ext[self.y0:self.y1, self.x0:self.x1, ...]
            cropped_img = resize(cropped_img, (self.out_size[0]-2*gap, self.out_size[1]-2*gap), order=self.order, preserve_range=True)
            cropped_img = np.pad(cropped_img, ((gap,gap),(gap,gap)), mode='constant')
            cropped_imgs.append(cropped_img)
            imh, imw = img.shape[:2]
            roi = [np.clip(self.y0-pad_l,0,imh),
                   np.clip(self.x0-pad_l,0,imw),
                   np.clip(self.y1-pad_l,0,imh),
                   np.clip(self.x1-pad_l,0,imw)]
            rois.append(roi)

        if len(imgs) == 1:
            cropped_imgs = cropped_imgs[0]
            rois = rois[0]
        return cropped_imgs, rois

class Resizer:
    def __init__(self, img_shape, out_shape, keep_aspect=True, order=1, pad_val=0):
        self.img_shape = img_shape
        self.out_shape = out_shape
        self.pad_val = pad_val
        oh, ow = out_shape
        out_hw_rate = oh / ow

        imh, imw = img_shape[:2]

        if keep_aspect:
            hw_rate = imh / imw
            if hw_rate > out_hw_rate:
                imh1 = imh
                imw1 = int(imh / out_hw_rate)
                pad_w = int((imw1-imw)/2)
                self.pad = ((0,0),(pad_w, imw1-imw-pad_w),(0,0))
                self.rate = oh / imh1
            else:
                imw1 = imw
                imh1 = int(imw * out_hw_rate)
                pad_h = int((imh1 - imh) / 2)
                self.pad = ((pad_h, imh1-imh-pad_h),(0,0),(0,0))
                self.rate = ow / imw1
        else:
            self.pad = None
            self.rate_x = ow/imw
            self.rate_y = oh/imh
        self.order = order

    def __call__(self, d):
        if isinstance(d, np.ndarray) and (d.shape[-1] == 3 or d.ndim == 2):
            return self.apply_img(d)
        else:
            return self.apply_regions(d)

    def apply_img(self, img):
        if self.pad:
            img = np.lib.pad(img, self.pad[:img.ndim], mode='constant', constant_values=self.pad_val)
        return resize(img, self.out_shape, preserve_range=True, order=self.order).astype(img.dtype)

    def apply_regions(self, regions):
        if self.pad:
            return [[[
                int((x + self.pad[1][0])*self.rate),
                int((y + self.pad[0][0])*self.rate),
            ] for x, y in kps] for kps in regions]
        else:
            return [[[
                int(x*self.rate_x),
                int(y*self.rate_y),
            ] for x, y in kps] for kps in regions]

def find_largest_connected_component(img):
    new_img = np.zeros_like(img)
    for val in np.unique(img)[1:]:
        mask = (img == val).astype('u1')
        labels, stats = cv2.connectedComponentsWithStats(mask, 4)[1:3]
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        new_img[labels == largest_label] = val
    return new_img

def fit_rotated_box(bin_img):
    bin_img = find_largest_connected_component(bin_img)
    ret, contours, hierarchy = cv2.findContours(bin_img, 1, 2)
    contour = contours[0]
    M = cv2.moments(contour)
    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    return cv2.minAreaRect(contour)

class AffineMapper:
    def __init__(self, src_pts, to_shape, from_shape=None):
        self.imh, self.imw = to_shape
        dst_pts = np.asarray([[0, self.imh], [0, 0],
                              [self.imw, 0], [self.imw, self.imh]], dtype='f4')
        self.aff = cv2.getAffineTransform(src_pts[:3], dst_pts[:3])
        if from_shape:
            self.aff_inv = cv2.invertAffineTransform(self.aff)
            self.from_shape = from_shape

    def __call__(self, *imgs, order=1):
        out = [cv2.warpAffine(img, self.aff, (self.imw, self.imh), flags=order) for img in imgs]
        if len(imgs) == 1:
            return out[0]
        return out

    def reverse(self, *imgs, order=1):
        out = [cv2.warpAffine(img, self.aff_inv, (self.from_shape[1], self.from_shape[0]), flags=order) for img in imgs]
        if len(imgs) == 1:
            return out[0]
        return out

def get_rotated_crop_transformer(bin_img, crop_ratio, to_shape):
    crop_w_ratio, crop_h_ratio = crop_ratio
    rbox = list(fit_rotated_box(bin_img))
    rbox[1] = [rbox[1][0]*crop_w_ratio, rbox[1][1]*crop_h_ratio]
    rbox_xs = cv2.boxPoints(tuple(rbox))
    transformer = AffineMapper(rbox_xs, to_shape, from_shape=bin_img.shape)
    return transformer

def preprocess_grays(imgs, img_shape, mean=128, std=128, expand_chn=1, dtype='f4'):
    imgs = [to_gray(i).astype(dtype) for i in imgs]
    if tuple(imgs[0].shape[:2]) != img_shape:
        imgs = [resize(i, img_shape, preserve_range=True) for i in imgs]
    imgs = np.asarray(imgs)
    imgs = (imgs - mean) / std
    if expand_chn == 1:
        imgs = imgs[:,None,:,:]
    return imgs
