%define		mod_name	auth_kerb
%define 	apxs	/usr/sbin/apxs
Summary:	This is the Kerberos authentication module for Apache
Summary(pl):	Modu³ uwierzytelnienia Kerberos dla Apache
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
Patch1:     	%{name}-aprfix.patch
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
authenticate HTTP clients using user entries in an Kerberos directory.

%description -l pl
To jest modu³ uwierzytelnienia dla Apache pozwalaj±cy na
uwierzytelnianie klientów HTTP z u¿yciem wpisów w katalogu Kerberosa.

%prep
%setup -q -n mod_%{mod_name}-%{version}-%{pre}
%patch1 -p1

%build
%configure
%{__make}

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
