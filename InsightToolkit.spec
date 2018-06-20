%define _ver_major      4
%define _ver_minor      13
%define _ver_release    0
%define _ver_doc_major    4
%define _ver_doc_minor    13
%define _ver_doc_release  0

%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           InsightToolkit
Summary:        Insight Toolkit library for medical image processing
Version:        %{_ver_major}.%{_ver_minor}.%{_ver_release}
Release:        7%{?dist}
License:        ASL 2.0
Group:          Applications/Engineering
Source0:        http://sourceforge.net/projects/itk/files/itk/%{_ver_major}.%{_ver_minor}/%{name}-%{version}.tar.xz
Source1:        http://downloads.sourceforge.net/project/itk/itk/%{_ver_doc_major}.%{_ver_doc_minor}/InsightSoftwareGuide-Book1-%{_ver_doc_major}.%{_ver_doc_minor}.%{_ver_doc_release}.pdf
Source2:        http://downloads.sourceforge.net/project/itk/itk/%{_ver_doc_major}.%{_ver_doc_minor}/InsightSoftwareGuide-Book2-%{_ver_doc_major}.%{_ver_doc_minor}.%{_ver_doc_release}.pdf
Source3:        http://sourceforge.net/projects/itk/files/itk/%{_ver_major}.%{_ver_minor}/InsightData-%{version}.tar.xz
URL:            http://www.itk.org/
Patch0:         %{name}-0001-Set-lib-lib64-according-to-the-architecture.patch

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  fftw-devel
BuildRequires:  castxml
BuildRequires:  gdcm-devel
BuildRequires:  graphviz
BuildRequires:  hdf5-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libxml2-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-devel
BuildRequires:  python2-devel
BuildRequires:  qtwebkit-devel
BuildRequires:  vxl-devel >= 1.17.0.2017
BuildRequires:  vtk-devel
BuildRequires:  zlib-devel
BuildRequires:  blas-devel
BuildRequires:  lapack-devel
BuildRequires:  netcdf-cxx-devel
BuildRequires:  jsoncpp-devel
BuildRequires:  expat-devel
BuildRequires:  libminc-devel
BuildRequires:  dcmtk
BuildRequires:  gtest-devel

%description
ITK is an open-source software toolkit for performing registration and
segmentation. Segmentation is the process of identifying and classifying data
found in a digitally sampled representation. Typically the sampled
representation is an image acquired from such medical instrumentation as CT or
MRI scanners. Registration is the task of aligning or developing
correspondences between data. For example, in the medical environment, a CT
scan may be aligned with a MRI scan in order to combine the information
contained in both.

ITK is implemented in C++ and its implementation style is referred to as
generic programming (i.e.,using templated code). Such C++ templating means
that the code is highly efficient, and that many software problems are
discovered at compile-time, rather than at run-time during program execution.

%package        devel
Summary:        Insight Toolkit development files
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-vtk-devel%{?_isa} = %{version}-%{release}

%description devel
Insight Tookkit development files.

%package        examples
Summary:        C++, Tcl and Python example programs/scripts for ITK
Group:          Development/Languages
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description examples
ITK examples

%package        doc
Summary:        Documentation for ITK
Group:          Documentation
BuildArch:      noarch

%description    doc
Insight Tookit additional documentation.

# Hit bug http://www.gccxml.org/Bug/view.php?id=13372
# We agreed with Mattias Ellert to postpone the bindings till
# next gccxml update.
# %package        python
# Summary:        Documentation for ITK
# Group:          Documentation
# BuildArch:      noarch

# %description    python
# Python bindings for ITK.

%package        vtk
Summary:        Provides an interface between ITK and VTK
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description vtk
Provides an interface between ITK and VTK

%package        vtk-devel
Summary:        Libraries and header files for development of ITK-VTK bridge
Group:          Development/Libraries
Requires:       %{name}-vtk%{?_isa} = %{version}-%{release}
Requires:       vtk-devel%{?_isa}

%description vtk-devel
Libraries and header files for development of ITK-VTK bridge

%prep
%autosetup -p1

# copy guide into the appropriate directory
cp -a %{SOURCE1} %{SOURCE2} .

# remove applications: they are shipped separately now
rm -rf Applications/

# remove source files of external dependencies that itk gets linked against
# DICOMParser, GIFTI, KWSys, MetaIO, NrrdIO, Netlib, VNLInstantiation are not
# yet in Fedora
# DoubleConversion still seems to need the source present
# NIFTI needs support - https://issues.itk.org/jira/browse/ITK-3349
# OpenJPEG - https://issues.itk.org/jira/browse/ITK-3350
find Modules/ThirdParty/* \( -name DICOMParser -o -name DoubleConversion -o -name GIFTI -o -name KWSys -o -name MetaIO -o -name NIFTI -o -name NrrdIO -o -name Netlib -o -name OpenJPEG -o name VNLInstantiation -o -name GoogleTest \) \
    -prune -o -regextype posix-extended -type f \
    -regex ".*\.(h|hxx|hpp|c|cc|cpp|cxx|txx)$" -not -iname "itk*" -print0 | xargs -0 rm -fr

tar xJvf %{SOURCE3} -C ..

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}

%cmake .. \
       -DBUILD_SHARED_LIBS:BOOL=ON \
       -DBUILD_EXAMPLES:BOOL=ON \
       -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"\
       -DCMAKE_VERBOSE_MAKEFILE=ON\
       -DCMAKE_CXX_FLAGS:STRING="%{optflags}" \
       -DBUILD_TESTING=ON\
       -DITK_FORBID_DOWNLOADS=ON \
       -DITKV3_COMPATIBILITY:BOOL=OFF \
       -DITK_BUILD_DEFAULT_MODULES:BOOL=ON \
       -DITK_USE_KWSTYLE:BOOL=OFF \
       -DModule_ITKVtkGlue:BOOL=ON \
       -DITK_WRAP_PYTHON:BOOL=OFF \
       -DITK_WRAP_JAVA:BOOL=OFF \
       -DBUILD_DOCUMENTATION:BOOL=OFF \
       -DModule_ITKReview:BOOL=ON \
       -DITK_USE_FFTWD=ON \
       -DITK_USE_FFTWF=ON \
       -DITK_USE_SYSTEM_LIBRARIES:BOOL=ON \
       -DITK_USE_SYSTEM_CASTXML=ON \
       -DITK_USE_SYSTEM_DCMTK=ON \
       -DITK_USE_SYSTEM_EXPAT=ON \
       -DITK_USE_SYSTEM_FFTW=ON \
       -DITK_USE_SYSTEM_GDCM=ON \
       -DITK_USE_SYSTEM_HDF5=ON \
       -DITK_USE_SYSTEM_JPEG=ON \
       -DITK_USE_SYSTEM_MINC=ON \
       -DITK_USE_SYSTEM_PNG=ON \
       -DITK_USE_SYSTEM_SWIG=ON \
       -DITK_USE_SYSTEM_TIFF=ON \
       -DITK_USE_SYSTEM_ZLIB=ON \
       -DITK_USE_SYSTEM_VXL=ON \
       -DITK_USE_SYSTEM_GOOGLETEST=ON \
       -DITK_INSTALL_LIBRARY_DIR=%{_lib}/ \
       -DITK_INSTALL_INCLUDE_DIR=include/%{name} \
       -DITK_INSTALL_PACKAGE_DIR=%{_lib}/cmake/%{name}/ \
       -DITK_INSTALL_RUNTIME_DIR:PATH=%{_bindir} \
       -DITK_INSTALL_DOC_DIR=share/doc/%{name}/

popd

%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}

# I dont know why this is necessary.
# Otherwise I can't build elatix
sed -i 's/GTest::GTest;GTest::Main/gtest/' ${RPM_BUILD_ROOT}%{_libdir}/cmake/InsightToolkit/Modules/ITKGoogleTest.cmake

# Install examples
mkdir -p %{buildroot}%{_datadir}/%{name}/examples
cp -ar Examples/* %{buildroot}%{_datadir}/%{name}/examples/

for f in LICENSE NOTICE README.md ; do
    cp -p $f ${RPM_BUILD_ROOT}%{_docdir}/%{name}/${f}
done

%files
%{_docdir}/%{name}/
%{_libdir}/*.so.*
%exclude %{_libdir}/libITKVtkGlue*.so.*
%{_bindir}/itkTestDriver

%files devel
%{_libdir}/*.so
%exclude %{_libdir}/libITKVtkGlue*.so
%{_libdir}/cmake/%{name}/
%{_includedir}/%{name}/
%exclude %{_includedir}/%{name}/itkImageToVTKImageFilter.h*
%exclude %{_includedir}/%{name}/itkVTKImageToImageFilter.h*
%exclude %{_includedir}/%{name}/QuickView.h
%exclude %{_includedir}/%{name}/vtkCaptureScreen.h
%exclude %{_libdir}/cmake/%{name}/Modules/ITKVtkGlue.cmake

%files examples
%{_datadir}/%{name}/examples

%files doc
%dir %{_docdir}/%{name}/
%{_docdir}/%{name}/*
%doc InsightSoftwareGuide-Book1-%{_ver_doc_major}.%{_ver_doc_minor}.%{_ver_doc_release}.pdf
%doc InsightSoftwareGuide-Book2-%{_ver_doc_major}.%{_ver_doc_minor}.%{_ver_doc_release}.pdf

%files vtk
%{_libdir}/libITKVtkGlue*.so.*

%files vtk-devel
%{_libdir}/libITKVtkGlue*.so
%{_includedir}/%{name}/itkImageToVTKImageFilter.h*
%{_includedir}/%{name}/itkVTKImageToImageFilter.h*
%{_includedir}/%{name}/QuickView.h
%{_includedir}/%{name}/vtkCaptureScreen.h
%{_libdir}/cmake/%{name}/Modules/ITKVtkGlue.cmake

%changelog
* Tue Jun 19 2018 Mark Harfouche <mark.harfouche@gmail.com> - 4.13.0-7
- Use system gtest

* Tue Jun 19 2018 Mark Harfouche <mark.harfouche@gmail.com> - 4.13.0-6
- rebuilt

* Tue Jun 19 2018 Mark Harfouche <mark.harfouche@gmail.com> - 4.13.0-5
- Added a fix for the GTest library in ITK cmake's definitions

* Tue Jun 19 2018 Mark Harfouche <mark.harfouche@gmail.com> - 4.13.0-4
- rebuilt without manually setting the -j parameter

* Tue Jun 19 2018 Mark Harfouche <mark.harfouche@gmail.com> - 4.13.0-2
- README.txt -> README.md following upstream

* Tue Jun 19 2018 Mark Harfouche <mark.harfouche@gmail.com> - 4.13.0-1
- rebuilt without `-j4`

* Sun Jun 17 2018 Mark Harfouche <mark.harfouche@gmail.com> - 4.13.0-0
- Version update

* Mon Aug 07 2017 Björn Esser <besser82@fedoraproject.org> - 4.9.1-7
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.9.1-4
- Patch to fix FTBFS (#1423098)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 7 2016 Orion Poplawski <orion@cora.nwra.com> - 4.9.1-3
- Rebuild for vtk 7.1

* Sat Jul 02 2016 Orion Poplawski <orion@cora.nwra.com> - 4.9.1-2
- Rebuild for hdf5 1.8.17

* Wed Apr 13 2016 Sebastian Pölsterl <sebp@k-d-w.org> - 4.9.1-1
- Update to 4.9.1

* Thu Mar 03 2016 Sebastian Pölsterl <sebp@k-d-w.org> - 4.9.0-1
- Update to 4.9.0 (#1303377)
- Use system MINC and DCMTK
- Really disable ITKv3 compatibility (#1290564)
- Compile using C++98 standard (VXL does not support C++11, yet)

* Fri Jan 22 2016 Orion Poplawski <orion@cora.nwra.com> - 4.8.2-3
- Rebuild for netcdf 4.4.0

* Sun Jan 03 2016 Sebastian Pölsterl <sebp@k-d-w.org> - 4.8.2-2
- Disable ITKv3 compatibility (#1290564)

* Sun Nov 15 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 4.8.2-1
- Update to 4.8.2

* Sun Nov 01 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 4.8.1-4
- Rebuilt for gdcm 2.6.1

* Thu Oct 29 2015 Orion Poplawski <orion@cora.nwra.com> - 4.8.1-3
- Rebuild for vtk 6.3.0

* Mon Oct 12 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 4.8.1-2
- Fix build using castxml and SSE patch

* Sun Oct 11 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 4.8.1-1
- Update to 4.8.1
- Build with castxml

* Fri Jul 03 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 4.8.0-2
- Include tarball that contains test data
- Update software guide

* Fri Jul 03 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 4.8.0-1
- Update to 4.8.0
- Enable single and double precision for FFT (fixes bug #1076793)

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 Orion Poplawski <orion@cora.nwra.com> - 4.7.2-3
- Add patch for sse includes

* Wed May 20 2015 Sebastian <sebp@k-d-w.org> - 4.7.2-3
- rebuilt

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 4.7.2-2
- Rebuild for hdf5 1.8.15

* Sat May 02 2015 Sebastian <sebp@k-d-w.org> - 4.7.2-1
- Update to 4.7.2

* Thu Mar 19 2015 Orion Poplawski <orion@cora.nwra.com> - 4.7.1-2
- Rebuild for vtk 6.2.0

* Fri Mar 06 2015 Sebastian <sebp@k-d-w.org> - 4.7.1-3
- Rebuilt for vtk

* Thu Mar 05 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 4.7.1-2
- Add vtk-devel to requires of devel (another fix for bug #1196315)
- Move ITKVtkGlue.cmake to vtk-devel subpackage

* Wed Feb 25 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 4.7.1-1
- Update to 4.7.1
- Add vtk-devel package (fixes bug #1196315)

* Thu Jan 08 2015 Orion Poplawski <orion@cora.nwra.com> - 4.7.0-3
- Rebuild for hdf5 1.8.14

* Sat Jan 03 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 4.7.0-2
- Fixed wrong version of software development guide

* Fri Jan 02 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 4.7.0-1
- Update to 4.7.0

* Fri Oct 03 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 4.6.1-1
- Update to 4.6.1
- Don't compile with -fpermissive

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 4.6.0-2
- Remove source files of external dependencies
- Partially fixes bug #1076793

* Mon Aug 04 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 4.6.0-1
- Update to 4.6.0

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May  7 2014 Tom Callaway <spot@fedoraproject.org> - 4.5.2-2
- rebuild for new R without bundled blas/lapack

* Thu Apr 17 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 4.5.2-1
- Update to version 4.5.2

* Sun Feb 16 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 4.5.1-1
- Update to version 4.5.1

* Sun Jan 26 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 4.5.0-4
- Require netcdf-cxx-devel instead of netcdf-devel

* Sun Jan 26 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 4.5.0-3
- Add jsoncpp-devel to BuildRequires (needed for vtk 6.1)

* Sun Jan 26 2014 Sebastian Pölsterl <sebp@k-d-w.org> - 4.5.0-2
- Rebuilt for vtk 6.1 update

* Sun Dec 29 2013 Sebastian Pölsterl <sebp@k-d-w.org> - 4.5.0-1
- Update to version 4.5.0
- Update software guide to 4.5.0
- Include LICENSE, NOTICE and README.txt in base package
- Move ITK-VTK bridge to new vtk subpackage
- Add BuildRequires on netcdf-devel (required by vtk)

* Mon Dec 23 2013 Sebastian Poelsterl <sebp@k-d-w.org> - 4.4.2-6
- Add BuildRequires on blas-devel and lapack-devel

* Mon Dec 23 2013 Sebastian Poelsterl <sebp@k-d-w.org> - 4.4.2-5
- Rebuilt for updated vtk

* Tue Oct 29 2013 Mario Ceresa <mrceresa@fedoraproject.org> - 4.4.2-4
- Revision bump up to build against updated gdcm

* Fri Oct 25 2013 Sebastian Pölsterl <sebp@k-d-w.org> - 4.4.2-3
- Removed HDF5 patch that seems to interfere with cmake 2.8.12

* Tue Oct 22 2013 Sebastian Pölsterl <sebp@k-d-w.org> - 4.4.2-2
- Rebuilt for gdcm 2.4.0

* Sun Sep 08 2013 Sebastian Pölsterl <sebp@k-d-w.org> - 4.4.2-1
- Update to version 4.4.2
- Added patch to only link against HDF5 release libraries

* Wed Aug 14 2013 Mario Ceresa <mrceresa@fedoraproject.org> 4.4.1-2
- Re-enabled vtk support
- Re-enabled tests
- Added BR qtwebkit

* Tue Aug 13 2013 Sebastian Pölsterl <sebp@k-d-w.org> - 4.4.1-1
- Update to version 4.4.1

* Mon Aug 05 2013 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 4.4.0-6
- Use unversioned doc
- Fixed bogus dates
- Temporary remove vtk support because of issues with texlive in rawhide

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Mario Ceresa <mrceresa@fedoraproject.org> 4.4.0-4
- Use xz tarball to save space in srpm media. (Fixes BZ980599)

* Fri Jul 12 2013 Orion Poplawski <orion@cora.nwra.com> 4.4.0-3
- Rebuild for vtk 6.0.0

* Wed Jul 10 2013 Mario Ceresa mrceresa fedoraproject org 4.4.0-2
- Devel package now requires vtk-devel because it is build with itkvtkglue mod
- Minor cleanups

* Mon Jul 08 2013 Mario Ceresa mrceresa fedoraproject org 4.4.0-1
- Contributed by Sebastian Pölsterl <sebp@k-d-w.org>
- Updated to upstream version 4.4.0
- Add VTK Glue module
- Removed obsolete TIFF patch

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 4.3.1-12
- Rebuild for hdf5 1.8.11

* Thu May 2 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-11
- Rebuilt for gdcm 2.3.2

* Fri Apr 26 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-10
- Install itkTestDriver in default package
- Install libraries into _libdir and drop ldconfig file

* Tue Apr 23 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-9
- Changed license to ASL 2.0

* Mon Apr 22 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-8
- Build examples
- Making tests informative as we debug it with upstream
- Fixed cmake support file location
- Disabled python bindings for now, hit http://www.gccxml.org/Bug/view.php?id=13372

* Sat Apr 20 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-7
- Enabled v3.20 compatibility layer

* Thu Apr 18 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-6
- Removed unused patches

* Mon Apr 08 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-5
- Fixed failing tests

* Wed Apr 03 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-4
- Fixed build with USE_SYSTEM_TIFF

* Fri Mar 29 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-3
- Compiles against VXL with compatibility patches
- Enabled testing

* Tue Feb 12 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-2
- Reorganized sections
- Fixed patch naming
- Removed buildroot and rm in install section
- Removed cmake version constraint
- Changed BR libjpeg-turbo-devel to libjpeg-devel
- Preserve timestamp of SOURCE1 file.
- Fixed main file section
- Added noreplace

* Fri Jan 25 2013 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.3.1-1
- Updated to 4.3.1
- Fixed conflicts with previous patches
- Dropped gcc from BR
- Fixed tabs-vs-space
- Improved description
- Re-enabled system tiff
- Clean up the spec
- Sanitize use of dir macro
- Re-organized docs
- Fixed libdir and datadir ownership

* Wed Dec 12 2012 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.2.1-4
- Included improvements to the spec file from Dan Vratil

* Tue Dec 4 2012 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.2.1-3
- Build against system VXL

* Mon Nov 26 2012 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.2.1-2
- Reorganized install paths

* Tue Nov 20 2012 Mario Ceresa mrceresa fedoraproject org InsightToolkit 4.2.1-1
- Updated to new version

* Wed Nov 30 2011 Mario Ceresa mrceresa fedoraproject org InsightToolkit 3.20.1-1
- Updated to new version
- Added binary morphology code

* Fri May 27 2011 Mario Ceresa mrceresa fedoraproject org InsightToolkit 3.20.0-5
- Added cstddef patch for gcc 4.6

* Mon Jan 24 2011 Mario Ceresa mrceresa@gmail.com InsightToolkit 3.20.0-4
- Added the ld.so.conf file

* Mon Nov 22 2010 Mario Ceresa mrceresa@gmail.com InsightToolkit 3.20.0-3
- Updated to 3.20 release
- Added vxl utility and review material
- Applied patch from upstream to fix vtk detection (Thanks to Mathieu Malaterre)
- Added patch to install in the proper lib dir based on arch value
- Added patch to set datadir as cmake configuration files dir

* Sun Dec  6 2009 Mario Ceresa mrceresa@gmail.com InsightToolkit 3.16.0-2
- Fixed comments from revision: https://bugzilla.redhat.com/show_bug.cgi?id=539387#c8

* Tue Nov 17 2009 Mario Ceresa mrceresa@gmail.com InsightToolkit 3.16.0-1
- Initial RPM Release
