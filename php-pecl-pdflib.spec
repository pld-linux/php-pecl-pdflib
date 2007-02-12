%define		_modname	pdflib
%define		_smodname	pdf
%define		_status		stable
Summary:	%{_modname} - creating PDF on the fly with the PDFlib library
Summary(pl.UTF-8):   %{_modname} - tworzenie PDF "w locie" za pomocą biblioteki PDFlib
Name:		php-pecl-%{_modname}
Version:	1.0
Release:	2
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
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	zlib-devel
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-pear-%{_modname}
Obsoletes:	php-pdf < 3:5.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension wraps the PDFlib programming library for processing PDF
on the fly.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
To rozszerzenie "owija" bibliotekę PDFlib przeznaczoną do tworzenia
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
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_smodname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_smodname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_smodname}.so
