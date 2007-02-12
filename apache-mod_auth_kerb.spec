%define		mod_name	auth_kerb
%define 	apxs	/usr/sbin/apxs
Summary:	This is the Kerberos authentication module for Apache
Summary(pl.UTF-8):	Moduł uwierzytelnienia Kerberos dla Apache
Name:		apache-mod_%{mod_name}
Version:	5.0
%define pre rc6
Release:	0.%{pre}.1
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modauthkerb/mod_%{mod_name}-%{version}-%{pre}.tar.gz
# Source0-md5:	274edfb950af20ce6ef0ddcb7c20263a
Source1:	%{name}.conf
Patch1:		%{name}-aprfix.patch
URL:		http://modauthkerb.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	gdbm-devel
BuildRequires:	heimdal-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using user entries in an Kerberos directory.

%description -l pl.UTF-8
To jest moduł uwierzytelnienia dla Apache pozwalający na
uwierzytelnianie klientów HTTP z użyciem wpisów w katalogu Kerberosa.

%prep
%setup -q -n mod_%{mod_name}-%{version}-%{pre}
%patch1 -p1

%build
%configure
%{__sed} -i -e 's/-pthread/-lpthread/' Makefile
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install src/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/20_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
