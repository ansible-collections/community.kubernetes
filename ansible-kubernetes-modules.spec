Name:           ansible-kubernetes-modules
Version:        0.3.1
Release:        2%{?dist}
Summary:        Ansible role containing pre-release K8s modules 
License:        ASL 2.0
URL:            https://github.com/ansible/%{name}
Source0:        https://github.com/ansible/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

Requires: ansible >= 2.3.0.0
Requires: python-openshift = %{version}

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
* Fri Oct 06 2017 Jason Montleon <jmontleo@redhat.com> 0.3.1-2
- new package built with tito

* Fri Oct 06 2017 Jason Montleon <jmontleo@redhat.com>
- new package built with tito

* Fri May 12 2017 Jason Montleon <jmontleo@redhat.com> - 0.0.1-1
- initial package
