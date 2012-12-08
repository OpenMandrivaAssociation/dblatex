Name:		dblatex
Version:	0.3
Release:	6
Summary:	DocBook to LaTeX/ConTeXt Publishing
BuildArch:	noarch
Group:		Publishing
License:	GPLv2+
URL:		http://dblatex.sourceforge.net/
Source0:	http://downloads.sourceforge.net/dblatex/dblatex-%{version}.tar.bz2
Source1:        COPYING-docbook-xsl
Patch0:		dblatex-0.2.7-external-which.patch

%py_requires -d
BuildRequires:	libxslt-proc tetex imagemagick tetex-latex python-which
Requires:	tetex libxslt-proc docbook-dtd44-xml docbook-dtd45-xml xmltex tetex-latex imagemagick transfig
Requires(post): kpathsea
Requires(postun): kpathsea

%description
dblatex is a program that transforms your SGML/XMLDocBook
documents to DVI, PostScript or PDF by translating them
into pure LaTeX as a first process.  MathML 2.0 markups
are supported, too. It started as a clone of DB2LaTeX.

Authors:
--------
   Benoît Guillon <marsgui at users dot sourceforge dot net>
   Andreas Hoenen <andreas dot hoenen at arcor dot de>


%prep
%setup -q
%patch0 -p1 -b .external-which
rm -r lib/contrib

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
#%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT
# these are already in tetex-latex:
for file in bibtopic.sty enumitem.sty ragged2e.sty passivetex/; do
  rm -rf $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/misc/$file
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/dblatex
for file in ` find $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/ -name '*.sty' ` ; do 
  mv $file $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/dblatex/`basename $file`;
done

rm -rf $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/{misc,contrib/example,style}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dblatex
# shipped in %%docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/

sed -e 's/\r//' xsl/mathml2/README > README-xsltml
touch -r xsl/mathml2/README README-xsltml
cp -p %{SOURCE1} COPYING-docbook-xsl
chmod +x %{buildroot}/%{python_sitelib}/dbtexmf/dblatex/xetex/*.py

 
%files
%defattr(-,root,root,-)
%{_mandir}/man1/dblatex.1*
%doc COPYRIGHT docs/manual.pdf COPYING-docbook-xsl README-xsltml
%{python_sitelib}/dbtexmf/
%{python_sitelib}/dblatex-*.egg-info
%{_bindir}/dblatex
%{_datadir}/dblatex/
%{_datadir}/texmf/tex/latex/dblatex/
%dir %{_sysconfdir}/dblatex

%post
/usr/bin/texhash

%postun
/usr/bin/texhash



%changelog
* Tue Jun 07 2011 Alexandre Lissy <alissy@mandriva.com> 0.3-4mdv2011.0
+ Revision: 683092
- Reverting Requires for docbook-dtd-xml to docbook-dtd44-xml
- Adding Requires against docbook-dtd45-xml (because of mandriva bug #63027)

* Tue Jun 07 2011 Alexandre Lissy <alissy@mandriva.com> 0.3-3
+ Revision: 683078
- Changing Requires for DocBook from docbook-dtd44-xml to docbook-dtd-xml

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.3-2
+ Revision: 663755
- mass rebuild

* Fri Oct 29 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.3-1mdv2011.0
+ Revision: 590218
- change BR to tetex; texlive is in contrib and dblatex is in main
- let texlive-latex pull texlive
- update to 0.3

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt for 2010.1

* Sat Oct 10 2009 Anssi Hannula <anssi@mandriva.org> 0.2.9-3mdv2010.0
+ Revision: 456517
- allow both tetex and texlive to satisfy requires(post,postun) in order
  to match the regular requires

* Thu Sep 03 2009 Thierry Vignaud <tv@mandriva.org> 0.2.9-2mdv2010.0
+ Revision: 427534
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Sat Aug 16 2008 David Walluck <walluck@mandriva.org> 0.2.9-1mdv2009.0
+ Revision: 272768
- fix build
- 0.2.9

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.2.8-2mdv2009.0
+ Revision: 266555
- rebuild early 2009.0 package (before pixel changes)

  + David Walluck <walluck@mandriva.org>
    - remove Conflicts: tex4ht
    - import dblatex


* Sun Dec 16 2007 Patrice Dumas <pertusus@free.fr> - 0.2.8-2.1
- don't install in docbook directory, it is a link to a versioned 
  directory and may break upon docbook update (#425251,#389231)

* Sun Nov 25 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.8-1
- Update to 0.2.8

* Mon Nov 12 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-16
- convert spec to utf8
- change to gplv2+

* Mon Nov 12 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-15
- Add copyright info

* Mon Nov  5 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-14
- Req tetex-fonts for texhash
- Fix post, postun

* Sun Nov  4 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-13
- Add texhash

* Sun Nov  4 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-12
- Fix xsl link

* Sat Nov  3 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-12
- Various fixes from pertusus@free.fr:
- rm iconv stuff
- simplify docs installation

* Fri Nov  2 2007  <ndbecker2@gmail.com> - 0.2.7-11
- Various minor fixes

* Thu Nov  1 2007  <ndbecker2@gmail.com> - 0.2.7-10
- Add some reqs and brs
- rmdir /usr/share/dblatex/latex/{misc,contrib/example,style}

* Sat Oct 27 2007  <ndbecker2@gmail.com> - 0.2.7-9
- link /usr/share/dblatex/xsl -> /usr/share/sgml/docbook/xsl-stylesheets/dblatex
- rmdir /usr/share/dblatex/latex/{misc,specs,style}
- own /etc/dblatex
- change $(...) -> `...`
- Preserve timestamps on iconv

* Mon Oct 15 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-9
- mv all .sty files to datadir/texmf/tex/latex/dblatex
- Add Conflicts tetex-tex4ht
- mv all xsl stuff to datadir/sgml/docbook/xsl-stylesheets/dblatex/

* Mon Oct 15 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-8
- rm redundant latex files

* Tue Sep 25 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-8
- Fixed encodings in docs directory
- Install docs at correct location

* Fri Sep 21 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-7
- Revert back to GPLv2
- untabify

* Fri Sep 21 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-6
- Fix source URL
- Install all docs
- Tabify

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-5
- Add BR tetex-latex

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-4
- Add  BR tetex, ImageMagick

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-3
- Add BR libxslt 

* Wed Sep 19 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-2
- Add BR python-devel

* Fri Sep  7 2007 Neal Becker <ndbecker2@gmail.com> - 0.2.7-1
- Initial



