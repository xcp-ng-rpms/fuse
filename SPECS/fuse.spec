Name:           fuse
Version:        2.9.2
Release:        10%{?dist}
Summary:        File System in Userspace (FUSE) utilities

Group:          System Environment/Base
License:        GPL+
URL:            https://github.com/libfuse/libfuse
Source0:        https://github.com/libfuse/libfuse/releases/download/fuse_2_9_4/%{name}-%{version}.tar.gz
Source1:	%{name}.conf

Patch1:		fuse-0001-More-parentheses.patch
Patch2:		fuse-aarch64.patch
Patch3:		buffer_size.patch
Patch4:		libfuse-fix-crash-in-unlock_path.patch

Requires:       which
Conflicts:      filesystem < 3
BuildRequires:  libselinux-devel

Requires(preun): chkconfig

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE userspace tools to
mount a FUSE filesystem.

%package libs
Summary:        File System in Userspace (FUSE) libraries
Group:          System Environment/Libraries
License:        LGPLv2+
Conflicts:      filesystem < 3

%description libs
Devel With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE libraries.


%package devel
Summary:        File System in Userspace (FUSE) devel files
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig
License:        LGPLv2+
Conflicts:      filesystem < 3

%description devel
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains development files (headers,
pgk-config) to develop FUSE based applications/filesystems.


%prep
%setup -q
#disable device creation during build/install
sed -i 's|mknod|echo Disabled: mknod |g' util/Makefile.in
%patch1 -p1 -b .add_parentheses
%patch2 -p1 -b .aarch64
%patch3 -p1 -b .buffer_size
%patch4 -p1 -b .unlock_path_crash

%build
# Can't pass --disable-static here, or else the utils don't build
export MOUNT_FUSE_PATH="%{_sbindir}"
CFLAGS="%{optflags} -D_GNU_SOURCE -fPIE -pie -Wl,-z,relro,-z,now" %configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
# change from 4755 to 0755 to allow stripping -- fixed later in files
chmod 0755 %{buildroot}/%{_bindir}/fusermount

# Get rid of static libs
rm -f %{buildroot}/%{_libdir}/*.a
# No need to create init-script
rm -f %{buildroot}%{_sysconfdir}/init.d/fuse

# Install config-file
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}

# Delete pointless udev rules, which do not belong in /etc (brc#748204)
rm -f %{buildroot}%{_sysconfdir}/udev/rules.d/99-fuse.rules

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING FAQ Filesystems NEWS README README.NFS
%{_sbindir}/mount.fuse
%attr(4755,root,root) %{_bindir}/fusermount
%{_bindir}/ulockmgr_server
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_mandir}/man1/*
%{_mandir}/man8/*

%files libs
%doc COPYING.LIB
%{_libdir}/libfuse.so.*
%{_libdir}/libulockmgr.so.*

%files devel
%{_libdir}/libfuse.so
%{_libdir}/libulockmgr.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fuse.h
%{_includedir}/ulockmgr.h
%{_includedir}/fuse

%changelog
* Fri Jan 05 2018 Miklos Szeredi <mszeredi@redhat.com> - 2.9.2-10
- Fix crash in unlock_path() (rhbz#1527008)

* Fri Oct 27 2017 Miklos Szeredi <mszeredi@redhat.com> - 2.9.2-9
- Update URLs in specfile to point to github project

* Tue May 02 2017 Carlos Maiolino <cmaiolino@redhat.com> - 2.9.2-8
- Make buffer size match kernel max transfer size

* Thu May 19 2016 Carlos Maiolino <cmaiolino@redhat.com> - 2.9.2-7
- Enable PIE and RELRO check

* Tue Jun 17 2014 Brian Foster <bfoster@redhat.com> - 2.9.2-6
- Use kernel types not sys types.

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.9.2-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.9.2-4
- Mass rebuild 2013-12-27

* Sat May 18 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.9.2-3
- Removed pre-F12 stuff
- Dropped ancient dependency on initscripts and chkconfig

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Adam Jackson <ajax@redhat.com>
- Remove ancient Requires: kernel >= 2.6.14, FC6 was 2.6.18.

* Tue Oct 23 2012 Tom Callaway <spot@fedoraproject.org> - 2.9.2-1
- update to 2.9.2

* Tue Aug 28 2012 Tom Callaway <spot@fedoraproject.org> - 2.9.1-1
- update to 2.9.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 16 2012 Peter Lemenkov <lemenkov@gmail.com> - 2.8.7-1
- Ver. 2.8.7

* Sun Apr 15 2012 Kay Sievers <kay@redhat.com> - 2.8.6-4
- remove needless udev rule

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.8.6-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.8.6-1
- Ver. 2.8.6
- Dropped patch 3 - fixed upstream

* Thu Mar 03 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.8.5-5
- Use noreplace for /etc/fuse.conf

* Tue Feb 15 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.8.5-4
- Provide /etc/fuse.conf (see rhbz #292811)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Peter Lemenkov <lemenkov@gmail.com> 2.8.5-2
- Fixed rhbz #622255

* Tue Oct 26 2010 Peter Lemenkov <lemenkov@gmail.com> 2.8.5-1
- Ver. 2.8.5

* Tue Jun  8 2010 Peter Lemenkov <lemenkov@gmail.com> 2.8.4-1
- Ver. 2.8.4
- CVE-2009-3297 patch dropped (merged upstream)

* Tue Jan 26 2010 Peter Lemenkov <lemenkov@gmail.com> 2.8.1-4
- Fixed CVE-2009-3297 (rhbz #558833)

* Thu Nov 19 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.1-3
- Fixed udev rules (bz# 538606)

* Thu Nov 19 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.1-2
- Removed support for MAKEDEV (bz# 511220)

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.1-1
- Ver. 2.8.1

* Wed Aug 19 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.0-1
- Ver. 2.8.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Peter Lemenkov <lemenkov@gmail.com> 2.7.4-2
- Fixed BZ#479581

* Sat Aug 23 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.4-1
- Ver. 2.7.4

* Sat Jul 12 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.3-3
- Fixed initscripts (BZ#441284)

* Thu Feb 28 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.3-2
- Fixed BZ#434881

* Wed Feb 20 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.3-1
- Ver. 2.7.3
- Removed usergroup fuse
- Added chkconfig support (BZ#228088)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.7.2-2
- Autorebuild for GCC 4.3

* Mon Jan 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.2-1
- bump to 2.7.2
- fix license tag

* Sun Nov  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-9
- fix initscript to work with chkconfig

* Mon Oct  1 2007 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-8
- Added Require: which (BZ#312511)

* Fri Sep 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-7
- revert udev rules change

* Thu Sep 20 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-6
- change udev rules so that /dev/fuse is chmod 666 (bz 298651)

* Wed Aug 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-5
- fix open issue (bz 265321)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.7.0-4
- Rebuild for selinux ppc32 issue.

* Sun Jul 22 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-3
- put pkgconfig file in correct place
- enable compat symlinks for files in /bin

* Sat Jul 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-2
- redefine exec_prefix to /
- redefine bindir to /bin
- redefine libdir to %%{_lib}
- don't pass --disable-static to configure
- manually rm generated static libs

* Wed Jul 18 2007 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-1
- Version 2.7.0
- Redefined exec_prefix due to demands from NTFS-3G

* Wed Jun  6 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.5-2
- Add BR libselinux-devel (bug #235145)
- Config files properly marked as config (bug #211122)

* Sat May 12 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.5-1
- Version 2.6.5

* Thu Feb 22 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.3-2
- Fixed bug #229642

* Wed Feb  7 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.3-1
* Ver. 2.6.3

* Tue Dec 26 2006 Peter Lemenkov <lemenkov@gmail.com> 2.6.1-1
- Ver. 2.6.1

* Sat Nov 25 2006 Peter Lemenkov <lemenkov@gmail.com> 2.6.0-2
- fixed nasty typo (see bug #217075)

* Fri Nov  3 2006 Peter Lemenkov <lemenkov@gmail.com> 2.6.0-1
- Ver. 2.6.0

* Sun Oct 29 2006 Peter Lemenkov <lemenkov@gmail.com> 2.5.3-5
- Fixed udev-rule again

* Sat Oct  7 2006 Peter Lemenkov <lemenkov@gmail.com> 2.5.3-4
- Fixed udev-rule

* Tue Sep 12 2006 Peter Lemenkov <lemenkov@gmail.com> 2.5.3-3%{?dist}
- Rebuild for FC6

* Wed May 03 2006 Peter Lemenkov <lemenkov@newmail.ru> 2.5.3-1%{?dist}
- Update to 2.5.3

* Thu Mar 30 2006 Peter Lemenkov <lemenkov@newmail.ru> 2.5.2-4%{?dist}
- rebuild

* Mon Feb 13 2006 Peter Lemenkov <lemenkov@newmail.ru> - 2.5.2-3
- Proper udev rule

* Mon Feb 13 2006 Peter Lemenkov <lemenkov@newmail.ru> - 2.5.2-2
- Added missing requires

* Tue Feb 07 2006 Peter Lemenkov <lemenkov@newmail.ru> - 2.5.2-1
- Update to 2.5.2
- Dropped fuse-mount.fuse.patch

* Wed Nov 23 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.2-1
- Use dist

* Wed Nov 23 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.2-1
- Update to 2.4.2 (solves CVE-2005-3531)
- Update README.fedora

* Sat Nov 12 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.1-3
- Add README.fedora
- Add hint to README.fedora and that you have to be member of the group "fuse"
  in the description
- Use groupadd instead of fedora-groupadd

* Fri Nov 04 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.1-2
- Rename packages a bit
- use makedev.d/40-fuse.nodes
- fix /sbin/mount.fuse
- Use a fuse group to restict access to fuse-filesystems

* Fri Oct 28 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.1-1
- Initial RPM release.
