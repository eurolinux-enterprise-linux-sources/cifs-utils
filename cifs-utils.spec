#% define pre_release rc1
%define pre_release %nil

Name:           cifs-utils
Version:        4.8.1
Release:        18%{pre_release}%{?dist}
Summary:        Utilities for mounting and managing CIFS mounts

Group:          System Environment/Daemons
License:        GPLv3
URL:            http://linux-cifs.samba.org/cifs-utils/
BuildRoot:      %{_tmppath}/%{name}-%{version}%{pre_release}-%{release}-root-%(%{__id_u} -n)

Source0:        ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}%{pre_release}.tar.bz2

Patch0:         mount.cifs-fix-test-for-strtoul-failure-in-mount.cif.patch
Patch1:         mount.cifs-reacquire-CAP_DAC_READ_SEARCH-before-call.patch
Patch2:         manpage-add-sections-for-missing-mount-options.patch
Patch3:         mount.cifs-handle-ENOSPC-EFBIG-condition-properly-when-alt.patch
Patch4:         mount.cifs-check_newline-returns-EX_USAGE-on-error-n.patch
Patch5:         manpage-add-more-missing-entries-and-fix-wsize.patch
Patch6:         cifs-upcall-improve-selection-of-SPNs.patch
Patch7:         cifs-upcall-alternate-krb5-conf.patch
Patch8:         mount.cifs-no-duplicate-mtab-entry-on-remount.patch
Patch9:         mount.cifs-add-backupuidgid-options.patch
Patch10:        mount.cifs-fix-strtoul-result-tests.patch
Patch11:        cifs.upcall-use-krb5_sname_to_principal.patch
Patch12:        mount.cifs-dont-allow-unpriv-users-to-mount-on-dirs-they-cant-chdir.patch
Patch13:        cifs.idmap-add-cifs.idmap.patch
Patch14:        acltools-add-get-setcifsacl.patch
Patch15:        manpage-add-more-mount.cifs-options.patch
Patch16:        autoconf-add-enable-pie-and-enable-relro.patch
Patch17:        mount.cifs-special-handling-for-krb5-usernames.patch
Patch18:        contrib-add-a-set-of-sample-etc-request-key.d-files.patch
Patch19:        mount.cifs-fix-the-conflict-between-rwpidforward-and.patch
Patch20:        mount.cifs-running-out-of-addresses-is-not-a-system-.patch
Patch21:        cifs-utils-acl-and-idmap-fixes.patch

BuildRequires:  libcap-ng-devel libtalloc-devel krb5-devel keyutils-libs-devel autoconf automake samba-winbind-devel
Requires:       keyutils

%description
The SMB/CIFS protocol is a standard file sharing protocol widely deployed
on Microsoft Windows machines. This package contains tools for mounting
shares on Linux using the SMB/CIFS protocol. The tools in this package
work in conjunction with support in the kernel to allow one to mount a
SMB/CIFS share onto a client and use it as if it were a standard Linux
file system.

%prep
%setup -q -n %{name}-%{version}%{pre_release}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1

%build
%configure --prefix=/usr
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.idmap.conf %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.spnego.conf %{buildroot}%{_sysconfdir}/request-key.d

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc
/sbin/mount.cifs
%{_bindir}/getcifsacl
%{_bindir}/setcifsacl
%{_sbindir}/cifs.upcall
%{_sbindir}/cifs.idmap
%{_mandir}/man1/getcifsacl.1.gz
%{_mandir}/man1/setcifsacl.1.gz
%{_mandir}/man8/cifs.upcall.8.gz
%{_mandir}/man8/cifs.idmap.8.gz
%{_mandir}/man8/mount.cifs.8.gz
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.idmap.conf
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.spnego.conf

%changelog
* Fri Nov 09 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-18
- don't cast freely between wbcDomainSid and cifs_sid (bz 843612)

* Wed Nov 07 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-17
- fix printing of REVISION: and CONTROL: on BE arches (bz 843612)

* Wed Nov 07 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-16
- fix even more issues in cifs.idmap (bz 843617)
- fix even more issues in getcifsacl/setcifsacl (bz 843612)
- fixes for problems in setcifsacl found by coverity (bz 873683)

* Mon Nov 05 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-15
- fix several issues in cifs.idmap (bz 843617)
- fix several issues in getcifsacl/setcifsacl (bz 843612)

* Mon Oct 08 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-14
- fix return code when mount.cifs runs out of addresses to try (bz 856729)

* Wed Aug 29 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-13
- fix conflict between "rw" and "rwpidforward" mount options (bz 843596)

* Thu Aug 23 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-12
- add stock request-key config files in /etc/request-key.d (bz 843617)

* Wed Aug 22 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-11
- add cifs.idmap, binaries and autoconf goop (bz 843617)
- add getcifsacl and setcifsacl tools (bz 843612)
- add more missing mount.cifs options to manpage (bz 843596)
- enable PIE and RELRO (bz 838606)
- mount.cifs: handle usernames differently for sec=krb5 (bz 826825)

* Tue Apr 17 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-10
- mount.cifs: don't allow unprivileged users to mount onto dirs they can't chdir into (bz 812782)

* Thu Mar 29 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-9
- cifs.upcall: use krb5_sname_to_principal to construct principal name (bz 805490)

* Mon Mar 26 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-8
- mount.cifs: add backupuid=/backupgid= mount options (bz 806337)

* Fri Mar 02 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-7
- RFE: Improve selection of SPNs with cifs.upcall (bz 748757)
- mount.cifs does not use KRB5_CONFIG (bz 748756)
- mount -o remount <cifs> creates additional entries in /etc/mtab (bz 770004)
- mount.cifs does not honor the uid/gid=username option, only the uid/gid=# option (bz 796463)

* Mon Feb 20 2012 Jeff Layton <jlayton@redhat.com> 4.8.1-6
- undocumented mount.cifs options (bz 769923)

* Fri Jul 29 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-5
- fix handling of check_newline return code in mount.cifs (bz 725509)

* Mon Jul 25 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-4
- handle ENOSPC/EFBIG condition properly with altering mtab (bz 725509)

* Tue Jul 19 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-3
- mount.cifs: reacquire CAP_DAC_READ_SEARCH before calling mount (bz 676439)
- manpage: document missing mount.cifs options (bz 719363)

* Mon Apr 18 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-2
- mount.cifs: fix test for strtoul failure (bz 696951)

* Fri Jan 21 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-1
- rebase to version 4.8.1 which fixes autoconf problems in 4.8 (bz 669377)

* Wed Jan 19 2011 Jeff Layton <jlayton@redhat.com> 4.8-1
- rebase to version 4.8 for cruid= patches (bz 669377)

* Wed Jan 05 2011 Jeff Layton <jlayton@redhat.com> 4.7-4
- make cifs.upcall take the '-l' flag (bz 667382)
- fix segfault in cifs.upcall when passing an invalid option (bz 667382)

* Wed Jan 05 2011 Jeff Layton <jlayton@redhat.com> 4.7-3
- regenerate autoconf files for GSSAPI checksum patch (bz 645127)

* Tue Jan 04 2011 Jeff Layton <jlayton@redhat.com> 4.7-2
- rebase to version 4.7 (bz 658981)
- fix hardcoded paths in manpages (bz 658981)
- set GSSAPI checksum in SPNEGO blobs (bz 645127)

* Wed Jul 28 2010 Jeff Layton <jlayton@redhat.com> 4.4-5
- cifs.upcall: handle "creduid=" upcall parameter (bz 618609)

* Fri Apr 30 2010 Jeff Layton <jlayton@redhat.com> 4.4-4
- mount.cifs: fix bug in previous prefixpath patch (bz 586895)

* Thu Apr 29 2010 Jeff Layton <jlayton@redhat.com> 4.4-3
- mount.cifs: strip leading delimiter from prefixpath (bz 586895)

* Wed Apr 28 2010 Jeff Layton <jlayton@redhat.com> 4.4-2
- fix release tagging issue

* Wed Apr 28 2010 Jeff Layton <jlayton@redhat.com> 4.4-1
- update to 4.4

* Sat Apr 17 2010 Jeff Layton <jlayton@redhat.com> 4.3-2
- fix segfault when address list is exhausted (BZ#583230)

* Fri Apr 09 2010 Jeff Layton <jlayton@redhat.com> 4.3-1
- update to 4.3

* Fri Apr 02 2010 Jeff Layton <jlayton@redhat.com> 4.2-1
- update to 4.2

* Tue Mar 23 2010 Jeff Layton <jlayton@redhat.com> 4.1-1
- update to 4.1

* Mon Mar 08 2010 Jeff Layton <jlayton@redhat.com> 4.0-2
- fix bad pointer dereference in IPv6 scopeid handling

* Wed Mar 03 2010 Jeff Layton <jlayton@redhat.com> 4.0-1
- update to 4.0
- minor specfile fixes

* Fri Feb 26 2010 Jeff Layton <jlayton@redhat.com> 4.0-1rc1
- update to 4.0rc1
- fix prerelease version handling

* Mon Feb 08 2010 Jeff Layton <jlayton@redhat.com> 4.0a1-1
- first RPM package build

