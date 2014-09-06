Name:           mod_rpaf
Version:        0.6
Release:        1%{?dist}
License:        ASL 1.0
Group:          System Environment/Daemons
Requires:       httpd
Summary:        Changes the remote IP in Apache to use client IP and not proxy IP
URL:            http://stderr.net/apache/rpaf/
Source:         http://www.stderr.net/apache/rpaf/download/%{name}-%{version}.tar.gz
Source2:        mod_rpaf.conf

BuildRequires:  httpd-devel

Patch0:         mod_rpaf-0.6-fedora.patch

%define apxs /usr/bin/apxs
%define apache_libexecdir %(%{apxs} -q LIBEXECDIR)

%description
mod_rpaf changes the remote address of the client visible to other
Apache modules when two conditions are satisfied. First condition is
that the remote client is actually a proxy that is defined in
httpd configuration file. 
Secondly if there is an incoming X-Forwarded-For header and the proxy 
is in it's list of known proxies it takes the last IP from the incoming 
X-Forwarded-For header and changes the remote address of the client in 
the request structure. It also takes the incoming X-Host header and 
updates the virtual host settings accordingly.
For Apache2 mod_proxy it takes the X-Forwared-Host header and updates 
the virtual hosts.

%prep
%setup -qn %{name}-%{version}
%patch0 -p1

%build
make %{?_smp_mflags} APXS2=%{apxs} rpaf-2.0

%install
mkdir -p %{buildroot}/%{apache_libexecdir}
cp -p .libs/%{name}-2.0.so %{buildroot}/%{apache_libexecdir}/%{name}.so
install -D -m644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/httpd/conf.d/mod_rpaf.conf

%files
%doc CHANGES
%doc README
%{apache_libexecdir}/%{name}.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_rpaf.conf

%changelog -n mod_rpaf
* Wed Sep 07 2014 -  <konstantinjch@mail.ru> -
- Fix spec file for fedora 

* Wed Aug 22 2012 - Sebastien Caps <sebastien.caps@guardis.com> - 0.6-1.el6
- Fix spec file for package review
- Add configuration sample as doc 

* Tue Nov 16 2010 - Sebastien Caps <sebastien.caps@guardis.com> - 0.6-1.el5
- initial package for centos/rhel5
