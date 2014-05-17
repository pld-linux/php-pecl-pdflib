%define		php_name	php%{?php_suffix}
%define		modname	pdflib
%define		smodname	pdf
%define		status		stable
Summary:	%{modname} - creating PDF on the fly with the PDFlib library
Summary(pl.UTF-8):	%{modname} - tworzenie PDF "w locie" za pomocą biblioteki PDFlib
Name:		%{php_name}-pecl-%{modname}
Version:	2.1.9
Release:	5
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	04b4e0a2a8731c5f087f40620aca4ddf
URL:		http://pecl.php.net/package/pdflib/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	pdflib-devel
BuildRequires:	rpmbuild(macros) >= 1.650
BuildRequires:	zlib-devel
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pdf < 3:5.0.0
Obsoletes:	php-pecl-pdflib < 2.1.9-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension wraps the PDFlib programming library for processing PDF
on the fly.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
To rozszerzenie "owija" bibliotekę PDFlib przeznaczoną do tworzenia
dokumentów PDF "w locie".

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
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

install -p modules/%{smodname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{smodname}.so
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
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{smodname}.so
