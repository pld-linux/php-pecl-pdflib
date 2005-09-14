%define		_modname	pdflib
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - creating PDF on the fly with the PDFlib library
Summary(pl):	%{_modname} - tworzenie PDF "w locie" za pomoc± biblioteki PDFlib
Name:		php-pecl-%{_modname}
Version:	1.0
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	60341f1afd61a6ec01790793473a702a
Patch0:		%{name}-fix_includes.patch
URL:		http://pecl.php.net/package/Modname/
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	pdflib-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.238
BuildRequires:	zlib-devel
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
Obsoletes:	php-pear-%{_modname}
Obsoletes:	php-pdf < 3:5.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension wraps the PDFlib programming library for processing PDF
on the fly.

In PECL status of this extension is: %{_status}.

%description -l pl
To rozszerzenie "owija" bibliotekê PDFlib przeznaczon± do tworzenia
dokumentów PDF "w locie".

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
%patch0 -p1

%build
cd %{_modname}-%{version}
phpize
%configure \
	--with-png-dir=%{_prefix} \
	--with-jpeg-dir=%{_prefix} \
	--with-tiff-dir=%{_prefix} \
	--with-zlib-dir=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/pdf.so $RPM_BUILD_ROOT%{extensionsdir}/%{_modname}.so
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
