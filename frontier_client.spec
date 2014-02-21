### RPM external frontier_client 2.8.10
## INITENV +PATH PYTHONPATH %{i}/python/lib

Source: http://frontier.cern.ch/dist/%{n}__%{realversion}__src.tar.gz
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif

Requires: expat
Requires: openssl
Requires: pacparser
Requires: python
%if "%online" != "true"
Requires: zlib
%else
Requires: onlinesystemtools
%endif

Patch0: frontier_client-2.8.5-fix-gcc47
Patch1: frontier_client-2.8.8-add-python-dbapi
Patch2: frontier_client.2.8.6.mic

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -n %{n}__%{realversion}__src

%if "%online" != "true"
%define makeargs "EXPAT_DIR=${EXPAT_ROOT} PACPARSER_DIR=${PACPARSER_ROOT} COMPILER_TAG=gcc_%{gccver} ZLIB_DIR=${ZLIB_ROOT}  OPENSSL_DIR=${OPENSSL_ROOT}"
%else
%define makeargs "EXPAT_DIR=${EXPAT_ROOT} PACPARSER_DIR=${PACPARSER_ROOT} COMPILER_TAG=gcc_%{gccver}"
%endif

%patch0 -p1
%patch1 -p1
%if "%mic" == "true"
%patch2 -p1
%endif

%build

export MAKE_ARGS=%{makeargs}
%if "%mic" == "true"
CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" make $MAKE_ARGS CXXFLAGS="%cms_cxxflags -ldl"
%else
 make $MAKE_ARGS CXXFLAGS="%cms_cxxflags -ldl"
%endif

%install
mkdir -p %i/lib
mkdir -p %i/include
export MAKE_ARGS=%{makeargs}
make $MAKE_ARGS CXXFLAGS="%cms_cxxflags -ldl" distdir=%i dist

case $(uname) in 
  Darwin ) 
    so=dylib 
    ln -sf libfrontier_client.%{realversion}.$so %i/lib/libfrontier_client.$so
    ln -sf libfrontier_client.$so.%{realversion} %i/libfrontier_client.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/").$so
    ;; 
  * ) 
    so=so 
    ln -sf libfrontier_client.$so.%{realversion} %i/lib/libfrontier_client.$so
    ln -sf libfrontier_client.$so.%{realversion} %i/lib/libfrontier_client.$so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")
    ;; 
esac

cp -r python %i

