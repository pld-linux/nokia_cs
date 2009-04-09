#TODO
#- NFY
#- udev rules
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel
%bcond_with	verbose		# verbose build (V=1)
#
%if !%{with kernel}
%undefine	with_dist_kernel
%endif
%define		srcname	d211_2_6
%define		rel	0.1
Summary:	nokia d211 multimode radio card module
Name:		nokia_cs
Version:	1.0
Release:	%{rel}
Epoch:		0
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/sourceforge/d211/%{srcname}.zip
# Source0-md5:	42a24f8ff461961a811f6d3f1bfcf48a
Source1:	http://dl.sourceforge.net/sourceforge/d211/dtools.c
# Source1-md5:	99a9cbd940ac8de8553aaac31b3d61b8
Patch0:		%{name}-CFLAGS.patch
URL:		http://d211.sourceforge.net/
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The driver for the nokia d211 multimode radio card for 2.6 kernels.

%package -n kernel%{_alt_kernel}-pcmcia-%{name}
Summary:	Linux driver for nokia d211 multimode radio card
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires:	module-init-tools >= 3.2.2-2
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-pcmcia-%{name}
The driver for the nokia d211 multimode radio card for 2.6 kernels.

This package contains Linux module.

%prep
%setup -q -n %{srcname}
cp -f %SOURCE1 src/

%patch0 -p0

%build
cd src
%build_kernel_modules -m %{name}

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m %{name} -d pcmcia -n %{name} -s current

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-pcmcia-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-pcmcia-%{name}
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-pcmcia-%{name}
%defattr(644,root,root,755)
/etc/modprobe.d/%{_kernel_ver}/%{name}.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/pcmcia/%{name}-current.ko*
