%define module usbvision 
%define version 0.9.8.3

Summary: The usbvision driver for some USB TV devices
Name: dkms-%{module}
Version: %{version}
Release:  %mkrel 3
License: GPL
Group: System/Kernel and hardware
Source0: http://ovh.dl.sourceforge.net/sourceforge/usbvision/%{module}-%{version}.tar.bz2
URL: http://usbvision.sf.net
Provides: %{module}
Requires: dkms >= 1.00
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root/

%description
This is a driver for the video grabber USBVision, a USB-only cable used in many
"webcam" devices.

%prep
%setup -n %{module} -q

%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/src/%{module}-%{version}-%{release}

cp -rf	*		$RPM_BUILD_ROOT/usr/src/%{module}-%{version}-%{release}
cat > %{buildroot}/usr/src/%{module}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_VERSION="%{version}-%{release}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{module}"
MAKE[0]="make -C \${kernel_source_dir} SUBDIRS=\${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build/src modules"
CLEAN="make -C \${kernel_source_dir} SUBDIRS=\${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build/src clean"

BUILT_MODULE_NAME[0]="\$PACKAGE_NAME"
BUILT_MODULE_LOCATION[0]="src"
DEST_MODULE_LOCATION[0]="/kernel/drivers/usb/media/usbvision/"

# To be removed when we will be able to compile 0.9.8.3
BUILT_MODULE_NAME[1]="saa7113"
BUILT_MODULE_LOCATION[1]="src"
DEST_MODULE_LOCATION[1]="/kernel/drivers/usb/media/usbvision/"

BUILT_MODULE_NAME[2]="i2c-algo-usb"
BUILT_MODULE_LOCATION[2]="src"
DEST_MODULE_LOCATION[2]="/kernel/drivers/usb/media/usbvision/"

AUTOINSTALL=yes
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/src/%{module}-%{version}-%{release}

%post
dkms add -m	%{module} -v %{version}-%{release} --rpm_safe_upgrade
dkms build -m	%{module} -v %{version}-%{release} --rpm_safe_upgrade
dkms install -m	%{module} -v %{version}-%{release} --rpm_safe_upgrade

%preun
dkms remove -m	%{module} -v %{version}-%{release} --rpm_safe_upgrade --all

