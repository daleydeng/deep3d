from realsense import pyrealsense2 as rs

DEPTH_UNIT = 0.001

def rs_get_fov(profile, mode):
    vid_profile = profile.get_stream(getattr(rs.stream, mode)).as_video_stream_profile()
    return rs.rs2_fov(vid_profile.get_intrinsics())

def rs_probe_fov(pipeline, config):
    profile = pipeline.start(config)
    dev = profile.get_device()
    depth_scale = dev.first_depth_sensor().get_depth_scale()
    assert abs(depth_scale - DEPTH_UNIT) < 1e-6

    color_fov = rs_get_fov(profile, mode='color')
    depth_fov = rs_get_fov(profile, mode='depth')
    pipeline.stop()
    return depth_fov, color_fov

def rs_create_pipeline(depth_size, depth_fps, color_size, color_fps):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, *depth_size, rs.format.z16, depth_fps)
    config.enable_stream(rs.stream.color, *color_size, rs.format.rgb8, color_fps)

    fov = rs_probe_fov(pipeline, config)
    return pipeline, config, fov
