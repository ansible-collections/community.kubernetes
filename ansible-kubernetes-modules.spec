Name:           ansible-kubernetes-modules
Version:        0.4.0
Release:        8%{?dist}
Summary:        Ansible role containing pre-release K8s modules
License:        ASL 2.0
URL:            https://github.com/ansible/%{name}
Source0:        https://github.com/ansible/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

Requires: ansible >= 2.3.0.0
Requires: python-openshift >= 0.4

%description
%{summary}

%prep
%autosetup -p1

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/ansible/roles/ansible.kubernetes-modules
mv * %{buildroot}%{_sysconfdir}/ansible/roles/ansible.kubernetes-modules

%check

%files
%{_sysconfdir}/ansible/roles/ansible.kubernetes-modules

%changelog
* Fri Jan 19 2018 David Zager <david.j.zager@gmail.com> 0.4.0-8
- when in checkmode _create returns None and cannot have to_dict() called (#27)
  (trbs@users.noreply.github.com)
- Show openshift version (chousekn@redhat.com)
- Unpin openshift (chousekn@redhat.com)
- regen modules (fabian@fabianism.us)
- Pin openshift. Trying Origin 3.6.7. (chousekn@redhat.com)

* Wed Jan 17 2018 David Zager <david.j.zager@gmail.com> 0.4.0-7
- Bump package version for 4.x (david.j.zager@gmail.com)
- Update releasers (david.j.zager@gmail.com)
- update generated modules (#26) (fabian@fabianism.us)

* Mon Oct 16 2017 Jason Montleon <jmontleo@redhat.com> 0.3.1-6
- Update to latest k8s_common (chousekn@redhat.com)

* Fri Oct 13 2017 Jason Montleon <jmontleo@redhat.com> 0.3.1-5
- increment release

* Fri Oct 13 2017 Jason Montleon <jmontleo@redhat.com> 0.3.1-4
- Bump version 

* Fri Oct 13 2017 Jason Montleon <jmontleo@redhat.com> 0.3.1-3
- add python-openshift rpm dependency (jmontleo@redhat.com)
- Travis file cleanup (#13) (chousekn@redhat.com)
- Removes -i inventory (chousekn@redhat.com)
- Removes ansible-galaxy install (chousekn@redhat.com)
- Regen modules. Add tests. (chousekn@redhat.com)
- Add Travis button (chousekn@redhat.com)
- Add simple module test (chousekn@redhat.com)
- Adds latest generated modules (chousekn@redhat.com)

* Fri Oct 06 2017 Jason Montleon <jmontleo@redhat.com> 0.3.1-2
- new package built with tito

* Fri Oct 06 2017 Jason Montleon <jmontleo@redhat.com>
- new package built with tito

* Fri May 12 2017 Jason Montleon <jmontleo@redhat.com> - 0.0.1-1
- initial package
