%define		mod_name	auth_kerb
%define 	apxs	/usr/sbin/apxs
Summary:	This is the kerb authentication module for Apache
Summary(pl):	Modu� autentykacji kerb dla Apache
Name:		apache-mod_%{mod_name}
Version:	5.0
%define pre rc4
Release:	0.%{pre}.1
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modauthkerb/mod_%{mod_name}-%{version}-%{pre}.tar.gz
# Source0-md5:	a717d5875e3f67c73b5d505ee4e46733
Source1:	%{name}.conf
URL:		http://modauthkerb.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	gdbm-devel
BuildRequires:	heimdal-devel
Requires(post,preun):	%{apxs}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using user entries in an kerb directory.

%description -l pl
To jest modu� autentykacji dla Apache pozwalaj�cy na autentykacj�
klient�w HTTP z u�yciem wpis�w w katalogu kerby.

%prep
%setup -q -n mod_%{mod_name}-%{version}-%{pre}

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd/httpd.conf}

install src/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/20_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_pkglibdir}/*
%{_sysconfdir}/httpd/httpd.conf/20_%{mod_name}.conf
