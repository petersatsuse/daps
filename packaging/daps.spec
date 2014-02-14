#
# spec file for package daps
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           daps
Version:        2.0~beta3
Release:        0

###############################################################
# 
# ATTENTION: Do NOT edit this file outside of
#            https://svn.code.sf.net/p/daps/svn/trunk/daps/packaging/daps.spec
#
#  Your changes will be lost on the next update
#  If you do not have access to the SVN repository, notify
#  <fsundermeyer@opensuse.org> or <toms@opensuse.org>
#  or send a patch
#
################################################################
#
# Please submit bugfixes or comments via https://sourceforge.net/p/daps/tickets
#

%define docbuilddir    %{_datadir}/daps
%define regcat         %{_bindir}/sgml-register-catalog
%define dbstyles       %{_datadir}/xml/docbook/stylesheet/nwalsh/current
%define daps_catalog   for-catalog-%{name}.xml

Summary:        DocBook Authoring and Publishing Suite
License:        GPL-2.0 or GPL-3.0
Group:          Productivity/Publishing/XML
Url:            http://sourceforge.net/p/daps
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}.rpmlintrc
Source2:        %{name}-fetch-source
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildArch:      noarch

BuildRequires:  bash >= 3.1
BuildRequires:  dia
BuildRequires:  docbook_4
BuildRequires:  docbook-xsl-stylesheets >= 1.77
BuildRequires:  fdupes
BuildRequires:  ghostscript-library
BuildRequires:  ImageMagick
BuildRequires:  inkscape
%if 0%{?suse_version} >= 1220
BuildRequires:  libxml2-tools
%endif
BuildRequires:  libxslt
#%%if %%sles_version >= 11
#BuildRequires:  sles-release
#%%else
#BuildRequires:  openSUSE-release
#%%endif
BuildRequires:  poppler-tools
BuildRequires:  python-xml
BuildRequires:  python-lxml
#BuildRequires:  sgml-skel
BuildRequires:  suse-xsl-stylesheets
BuildRequires:  svg-dtd
BuildRequires:  transfig
BuildRequires:  xml-commons-jaxp-1.3-apis
%if 0%{?suse_version} >= 1140
BuildRequires:  xmlgraphics-fop >= 0.94
%else
BuildRequires:  fop >= 0.94
%endif
#---
# Font stuff
BuildRequires:  fontpackages-devel


#
# In order to keep the requirements list as short as possible, only packages
# needed ti build EPUB, HTML and PDF are really required
# All other packages required for editing or more exotic output formats
# are recommended rather than required

PreReq:         libxml2
PreReq:         sgml-skel

Requires:       bash >= 3.1
Requires:       dia
Requires:       docbook_4
Requires:       docbook-xsl-stylesheets >= 1.77
Requires:       ghostscript-library
Requires:       ImageMagick
Requires:       inkscape
Requires:       libxslt
Requires:       make
Requires:       poppler-tools
Requires:       python-xml
Requires:       python-lxml
#Requires:       sgml-skel
Requires:       suse-xsl-stylesheets
Requires:       svg-schema
Requires:       transfig
Requires:       xml-commons-jaxp-1.3-apis
%if 0%{?suse_version} >= 1140
Requires:       xmlgraphics-fop >= 0.94
%else
Requires:       fop >= 0.94
%endif
Requires:       xmlstarlet

Recommends:     aspell aspell-en
%if 0%{?suse_version} < 1210
Recommends:     aspell-en-huge
%endif
Recommends:     daps-docmanager
Recommends:     docbook_5
Recommends:     epubcheck
Recommends:     exiftool
Recommends:     jing
Recommends:     optipng
%if 0%{?suse_version} >= 1140
Recommends:     perl-checkbot
%else
Recommends:     checkbot
%endif
Recommends:     remake
# Internal XEP package:
Recommends:     xep
Recommends:     xmlformat

Obsoletes:      susedoc < 4.3.32
Provides:       susedoc = 4.3.32

%description
DocBook Authoring and Publishing Suite (DAPS)

DAPS contains a set of stylesheets, scripts and makefiles that enable
you to create HTML, PDF, EPUB and other formats from DocBook XML with a
single command. It also contains tools to generate profiled source
tarballs for distributing your XML sources for translation or review.

DAPS also includes tools that assist you when writing DocBook XML:
linkchecker, validator, spellchecker, editor macros and stylesheets for
converting DocBook XML.

DAPS is the successor of susedoc. See
/usr/share/doc/packages/daps/README.upgrade_from_susedoc_4.x
for upgrade instructions.


#--------------------------------------------------------------------------
%prep
%setup -q -n %{name}
#%%patch1 -p1

#--------------------------------------------------------------------------
%build
%configure --docdir=%{_defaultdocdir}/%{name} --disable-edit-rootcatalog
%__make  %{?_smp_mflags}

#--------------------------------------------------------------------------
%install
make install DESTDIR=$RPM_BUILD_ROOT

# create symlinks:
%fdupes -s $RPM_BUILD_ROOT/%{_datadir}

#----------------------
%post
#
# XML Catalog entries for daps profiling
#
# remove existing entries first (if existing) - needed for
# zypper in, since it does not call postun
#
# delete ...
edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --del %{name}
# ... and add it again
edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --add /etc/xml/%{daps_catalog}

%reconfigure_fonts_post
exit 0

#----------------------
%postun
#
# delete catalog entry for daps profiling
# only run if package is really uninstalled ($1 = 0) and not
# in case of an update
#
if [ 0 = $1 ]; then 
if [ -x /usr/bin/edit-xml-catalog ] ; then
  edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --del %{name}
fi

%reconfigure_fonts_post
fi
exit 0

#----------------------
%posttrans
%reconfigure_fonts_posttrans

#----------------------
%files
%defattr(-,root,root)

%dir %{_ttfontsdir}
%dir %{_sysconfdir}/%{name}
%dir %{_defaultdocdir}/%{name}

%config %{_sysconfdir}/xml/*.xml
%config %{_sysconfdir}/%{name}/*

%doc %{_mandir}/man1/*.1%{ext_man}
%doc %{_defaultdocdir}/%{name}/*

%{_bindir}/*
%{_datadir}/emacs/site-lisp/docbook_macros.el
%{docbuilddir}
%{_ttfontsdir}/*
%exclude %{_defaultdocdir}/%{name}/INSTALL

#----------------------

%changelog
