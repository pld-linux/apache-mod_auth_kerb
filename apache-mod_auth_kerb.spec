%define		mod_name	auth_kerb
%define 	apxs	/usr/sbin/apxs
Summary:	This is the Kerberos authentication module for Apache
Summary(pl.UTF-8):	Moduł uwierzytelnienia Kerberos dla Apache
Name:		apache-mod_%{mod_name}
Version:	5.4
Release:	6
Epoch:		1
License:	GPL
Group:		Networking/Daemons/HTTP
Source0:	http://dl.sourceforge.net/modauthkerb/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	642b81763ad3ca81dba359cb952da5e3
Source1:	%{name}.conf
Patch0:		%{name}-heimdal.patch
Patch1:		%{name}-basic-auth.patch
URL:		http://modauthkerb.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	gdbm-devel
BuildRequires:	heimdal-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		apachelibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using user entries in an Kerberos directory.

%description -l pl.UTF-8
To jest moduł uwierzytelnienia dla Apache pozwalający na
uwierzytelnianie klientów HTTP z użyciem wpisów w katalogu Kerberosa.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1
%patch1 -p1

%build
%configure \
	--without-krb4 \
	--with-apache=%{_prefix}

%{__sed} -i -e 's/-pthread/-lpthread/' Makefile
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachelibdir},%{apacheconfdir}}

install src/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{apachelibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{apacheconfdir}/20_mod_%{mod_name}.conf

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{apachelibdir}/*.so
