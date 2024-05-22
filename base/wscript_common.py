from os import path
import sys
from waflib import Task
from waflib.TaskGen import extension
from waflib.Tools import c_preproc
from distutils.spawn import find_executable

class cuda(Task.Task):
    run_str = '${NVCC} ${NVCCFLAGS} -Xcompiler -fPIC --expt-relaxed-constexpr ${FRAMEWORKPATH_ST:FRAMEWORKPATH} ${CPPPATH_ST:INCPATHS} ${DEFINES_ST:DEFINES} ${CXX_SRC_F}${SRC} ${CXX_TGT_F} ${TGT}'
    color   = 'GREEN'
    ext_in  = ['.h', '.hh']
    vars    = ['CCDEPS']
    scan    = c_preproc.scan
    shell   = False

@extension('.cu', '.cu.cc')
def c_hook(self, node):
    return self.create_compiled_task('cuda', node)

def base_options_C(opt):
    opt.load('compiler_c compiler_cxx')
    opt.add_option('--sys', help='system prefix path for searching requirments')

def base_configure_C(conf, omp=False, cxx_std='11', cxx_only=False, intrinsics=False, O=3, use_cxx11_abi=True, use_cuda=False):
    if cxx_only:
        conf.load('compiler_cxx')
    else:
        conf.load('compiler_c compiler_cxx')
    env = conf.env
    env.append_value('CPPFLAGS', '-O{}'.format(O))
    if omp:
        env.append_value('CPPFLAGS', '-fopenmp')
        env.append_value('LDFLAGS', '-lgomp')
    if cxx_std:
        env.append_value('CXXFLAGS', '-std=c++'+cxx_std)
    if intrinsics:
        env.append_value('CPPFLAGS', ['-msse2', '-msse3', '-mpopcnt', '-msse4.1', '-msse4.2', '-mavx', '-mavx2'])

    if not use_cxx11_abi:
        env.prepend_value('CXXFLAGS', '-D_GLIBCXX_USE_CXX11_ABI=0')

    sys_prefix = conf.options.sys
    env.sys = sys_prefix
    if sys_prefix:
        inc_path = sys_prefix+'/include'
        env.prepend_value('CPPFLAGS', '-I'+inc_path)
        libpath = [sys_prefix+'/lib', sys_prefix+'/lib64']
        env.LIBPATH_SYS = libpath
        env.INCLUDES_SYS = inc_path
        for i in libpath:
            env.append_value('LDFLAGS', '-L'+i)
            env.append_value('RPATH', i)

    if use_cuda:
        cuda_base = path.dirname(find_executable('nvcc'))+'/..'
        cuda_inc = cuda_base+'/include'
        cuda_lib = cuda_base+'/lib64'
        env.INCLUDES_CUDA = cuda_inc
        env.LIBPATH_CUDA = cuda_lib
        env.LIB_CUDA = ['cudart', 'cudnn']
        conf.find_program('nvcc', var='NVCC')
        for f in env['CXXFLAGS']:
            nvflag = f
            if f.startswith('-std='):
                nvflag = '--std='+f[5:]
            elif f in ['-fPIC']:
                nvflag = '-Xcompiler '+f

            env.append_value('NVCCFLAGS', nvflag)

    if not conf.options.out:
        conf.options.out = 'build'
    env.OUT_DIR = conf.options.out
    env.append_value('RPATH', path.realpath(conf.options.out))

    if not conf.options.top:
        conf.options.top = '.'
    env.TOP_DIR = conf.options.top

    if sys.platform != 'win32':
        conf.check_cc(lib='m', uselib_store='m')
        env.append_value('LINKFLAGS_cshlib', ["-Wl,--unresolved-symbols=ignore-in-shared-libs", "-Wl,--as-needed"])

def bld_shlib(bld, **kws):
    if sys.platform == 'win32':
        if 'vnum' in kws:
            kws.pop('vnum')
        if 'cnum' in kws:
            kws.pop('cnum')
        if bld.env.get('WIN_STATIC', False):
            bld.stlib(**kws)
            return

    if 'install_path' not in kws:
        kws['install_path'] = '${PREFIX}/lib'
    bld.shlib(**kws)

def get_pysp_path(env):
    return '${PREFIX}/lib/'+env.LIB_python[0][:-1]+'/site-packages/'

def bld_pyclib(bld, **kws):
    env = bld.env
    if 'install_path' not in kws:
        kws['install_path'] = get_pysp_path(env) + kws['dst']
    env.cxxshlib_PATTERN = '%s.so'
    bld_shlib(bld, **kws)

def bld_pyclib_install_files(bld, dst, srcs):
    bld.install_files(get_pysp_path(bld.env)+dst, srcs)
