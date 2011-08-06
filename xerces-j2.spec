# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

#%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}
%define bootstrap %{?_with_bootstrap:1}%{!?_with_bootstrap:%{?_without_bootstrap:0}%{!?_without_bootstrap:%{?_bootstrap:%{_bootstrap}}%{!?_bootstrap:0}}}

%define cvs_version     2_7_1

Name:           xerces-j2
Version:        2.7.1
Release:        12.5%{?dist}
Epoch:          0
Summary:        Java XML parser
License:        ASL 2.0
URL:            http://xerces.apache.org/
Group:          Text Processing/Markup/XML
Source0:        http://archive.apache.org/dist/xml/xerces-j/Xerces-J-src.2.7.1.tar.gz
Source1:        %{name}-version.sh
Source2:        %{name}-constants.sh
Source3:        XJavac.java
Source4:        %{name}-MANIFEST.MF
Patch0:         %{name}-build.patch
Patch1:         %{name}-libgcj.patch
Obsoletes:      xerces-j2-dom3 < %{epoch}:%{version}-%{release}
Provides:       jaxp_parser_impl = 1.3
Provides:       xerces-j2-dom3 = %{epoch}:%{version}-%{release}
Requires:       xml-commons-apis >= 0:1.3
Requires:       xml-commons-resolver >= 1.1
BuildRequires:  java-devel
BuildRequires:  ant >= 0:1.6
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  jaxp_parser_impl
BuildRequires:  xml-commons-resolver >= 0:1.1
BuildRequires:  xml-commons-apis >= 0:1.3
%if ! %{bootstrap}
# xml-stylebook is not in Fedora yet
#BuildRequires:  xml-stylebook
BuildRequires:  xalan-j2
%endif
Requires(post): chkconfig jaxp_parser_impl
Requires(preun): chkconfig jaxp_parser_impl

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{gcj_support}
BuildRequires:      java-devel-gcj >= 1.5.0
Requires(post):         java-gcj >= 1.5.0
Requires(postun):       java-gcj >= 1.5.0
%endif

%description
Welcome to the future! Xerces2 is the next generation of high
performance, fully compliant XML parsers in the Apache Xerces family.
This new version of Xerces introduces the Xerces Native Interface (XNI),
a complete framework for building parser components and configurations
that is extremely modular and easy to program.

The Apache Xerces2 parser is the reference implementation of XNI but
other parser components, configurations, and parsers can be written
using the Xerces Native Interface. For complete design and
implementation documents, refer to the XNI Manual.

Xerces 2 is a fully conforming XML Schema processor. For more
information, refer to the XML Schema page.

Xerces 2 also provides a partial implementation of Document Object Model
Level 3 Core, Load and Save and Abstract Schemas [deprecated] Working
Drafts. For more information, refer to the DOM Level 3 Implementation
page.

%package        javadoc-impl
Summary:        Javadoc for %{name} implementation
Group:          Development/Documentation

%description    javadoc-impl
Javadoc for %{name} implementation.

%package        javadoc-apis
Summary:        Javadoc for %{name} apis
Group:          Development/Documentation
Obsoletes:      xerces-j2-dom3-javadoc < %{epoch}:%{release}-%{version}
Provides:       xerces-j2-dom3-javadoc = %{epoch}:%{release}-%{version}

%description    javadoc-apis
Javadoc for %{name} apis.

%package        javadoc-xni
Summary:        Javadoc for %{name} xni
Group:          Development/Documentation

%description    javadoc-xni
Javadoc for %{name} xni.

%package        javadoc-other
Summary:        Javadoc for other %{name} components
Group:          Development/Documentation

%description    javadoc-other
Javadoc for other %{name} components.

%if ! %{gcj_support}
%package        manual
Summary:        Documents for %{name}
Group:          Development/Documentation

%description    manual
%{summary}.
%endif

%package        demo
Summary:        Demo for %{name}
Group:          Development/Testing
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.

%package        scripts
Summary:        Additional utility scripts for %{name}
Group:          Text Processing/Markup/XML
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 0:1.6

%description    scripts
Additional utility scripts for %{name}.

%prep
%setup -q -n xerces-%{cvs_version}
%patch0 -b .build

mkdir -p tools/org/apache/xerces/util
cp -a %{SOURCE3} tools/org/apache/xerces/util
%patch1 -p0 -b .libgcj

%{__sed} -i 's/\r//' NOTICE

%build
pushd tools
javac -classpath $(build-classpath ant) org/apache/xerces/util/XJavac.java
mkdir bin && jar cf bin/xjavac.jar org/apache/xerces/util/XJavac.class
ln -sf $(build-classpath xml-commons-apis) .
ln -sf $(build-classpath xml-commons-resolver) .
%if ! %{bootstrap}
# Fedora does not have xml-stylebook yet
#ln -sf $(build-classpath xml-stylebook) .
ln -sf $(build-classpath xalan-j2) xalan.jar
%endif
popd

#%if ! %{gcj_support}
# Fedora does not have xml-stylebook yet
#export CLASSPATH=$(build-classpath xml-stylebook):tools/bin/xjavac.jar:build/xercesImpl.jar
export CLASSPATH=tools/bin/xjavac.jar:build/xercesImpl.jar
export ANT_OPTS="-Xmx256m -Djava.endorsed.dirs=$(pwd)/tools -Djava.awt.headless=true -Dbuild.sysclasspath=first -Ddisconnected=true"
#%endif
%if %{bootstrap}
ant \
        -Dbuild.compiler=modern \
        -Dtools.dir=%{_javadir} \
        -Djar.apis=xml-commons-apis.jar \
        -Djar.resolver=xml-commons-resolver.jar \
        clean jars javadocs
%else
%if ! %{gcj_support}
ant \
        -Dbuild.compiler=modern \
        -Djar.apis=xml-commons-apis.jar \
        -Djar.resolver=xml-commons-resolver.jar \
#        -Ddoc.generator.package=./tools/xml-stylebook.jar \
        clean jars javadocs docs sampjar
%else
ant \
        -Dbuild.compiler=modern \
        -Djar.apis=xml-commons-apis.jar \
        -Djar.resolver=xml-commons-resolver.jar \
        clean jars javadocs 
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE4} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/xercesImpl.jar META-INF/MANIFEST.MF

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/xercesImpl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *.jar; do ln -sf ${jar} dom3-${jar}; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-impl-%{version}
cp -pr build/docs/javadocs/xerces2/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-impl-%{version}
ln -s %{name}-impl-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-impl

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-apis-%{version}
cp -pr build/docs/javadocs/api/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-apis-%{version}
ln -s %{name}-apis-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-apis

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-xni-%{version}
cp -pr build/docs/javadocs/xni/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-xni-%{version}
ln -s %{name}-xni-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-xni

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-other-%{version}
cp -pr build/docs/javadocs/other/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-other-%{version}
ln -s %{name}-other-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-other

rm -rf build/docs/javadocs

# manual
%if ! %{gcj_support} && ! %{bootstrap}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr build/docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p ISSUES  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p LICENSE*  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p NOTICE  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p README  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p STATUS  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p TODO  $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%endif

# scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}-version
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/%{name}-constants

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p build/xercesSamples.jar \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}-samples.jar
cp -pr data $RPM_BUILD_ROOT%{_datadir}/%{name}

# jaxp_parser_impl ghost symlink
ln -s %{_sysconfdir}/alternatives \
  $RPM_BUILD_ROOT%{_javadir}/jaxp_parser_impl.jar

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-alternatives --install %{_javadir}/jaxp_parser_impl.jar \
  jaxp_parser_impl %{_javadir}/%{name}.jar 40

%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%preun
{
  [ $1 = 0 ] || exit 0
  update-alternatives --remove jaxp_parser_impl %{_javadir}/%{name}.jar
} >/dev/null 2>&1 || :

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%post demo
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun demo
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc [A-Z]*
%{_javadir}/%{name}*.jar
%{_javadir}/dom3-%{name}*.jar
%ghost %{_javadir}/jaxp_parser_impl.jar

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif

%files javadoc-impl
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-impl-%{version}
%doc %{_javadocdir}/%{name}-impl

%files javadoc-apis
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-apis-%{version}
%doc %{_javadocdir}/%{name}-apis

%files javadoc-other
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-other-%{version}
%doc %{_javadocdir}/%{name}-other

%files javadoc-xni
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-xni-%{version}
%doc %{_javadocdir}/%{name}-xni

%if ! %{gcj_support}
%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/[a-z]*
%endif

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-samples.jar.*
%endif

%files scripts
%defattr(0755,root,root,0755)
%{_bindir}/*


%changelog
* Wed Jan 20 2010 Andrew Overholt <overholt@redhat.com> - 0:2.7.1-12.5
- Version jaxp_parser_impl Provides.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:2.7.1-12.4
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.7.1-12.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.7.1-11.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.7.1-10.3
- Add osgi manifest.

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.7.1-10.2
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:2.7.1-10jpp.1
- Autorebuild for GCC 4.3

* Wed Mar 28 2007 Matt Wringe <mwringe@redhat.com> 0:2.7.1-9jpp.1
- Update with newest jpp version
- Clean up spec file for Fedora Review

* Sun Aug 13 2006 Warren Togami <wtogami@redhat.com> 0:2.7.1-7jpp.2
- fix typo in preun req

* Sat Aug 12 2006 Matt Wringe <mwringe at redhat.com> 0:2.7.1-7jpp.1
- Merge with upstream version

* Sat Aug 12 2006 Matt Wringe <mwringe at redhat.com> 0:2.7.1-7jpp
- Add conditional native compiling
- Add missing requires for javadocs
- Add missing requires for post and preun
- Update version to 7jpp at Fedora's request

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:2.7.1-6jpp_9fc
- Rebuilt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:2.7.1-6jpp_8fc
- rebuild

* Thu Mar 30 2006 Fernando Nasser <fnasser@redhat.com> 0:2.7.1-3jpp
- Add missing BR for xml-stylebook

* Wed Mar 22 2006 Ralph Apel <r.apel at r-apel.de> 0:2.7.1-2jpp
- First JPP-1.7 release
- use tools subdir and give it as java.endorsed.dirs (for java-1.4.2-bea e.g.)

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:2.7.1-6jpp_7fc
- stop scriptlet spew

* Wed Feb 22 2006 Rafael Schloming <rafaels@redhat.com> - 0:2.7.1-6jpp_6fc
- Updated to 2.7.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:2.6.2-6jpp_5fc
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:2.6.2-6jpp_4fc
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Archit Shah <ashah@redhat.com> 0:2.6.2-6jpp_3fc
- build xerces without using native code

* Mon Jan  9 2006 Archit Shah <ashah@redhat.com> 0:2.6.2-6jpp_2fc
- rebuilt for new gcj

* Wed Dec 21 2005 Jesse Keating <jkeating@redhat.com> 0:2.6.2-6jpp_1fc
- rebuilt for new gcj

* Tue Dec 13 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Oct 07 2005 Ralph Apel <r.apel at r-apel.de> 0:2.7.1-1jpp
- Upgrade to 2.7.1

* Thu Jul 21 2005 Ralph Apel <r.apel at r-apel.de> 0:2.6.2-7jpp
- Include target jars-dom3
- Create new subpackage dom3

* Mon Jul 18 2005 Gary Benson <gbenson at redhat.com> 0:2.6.2-5jpp_2fc
- Build on ia64, ppc64, s390 and s390x.
- Switch to aot-compile-rpm (also BC-compiles samples).

* Wed Jul 13 2005 Gary Benson <gbenson at redhat.com> 0:2.6.2-6jpp
- Build with Sun JDK (from <gareth.armstrong at hp.com>).

* Wed Jun 15 2005 Gary Benson <gbenson at redhat.com> 0:2.6.2-5jpp_1fc
- Upgrade to 2.6.2-5jpp.

* Tue Jun 14 2005 Gary Benson <gbenson at redhat.com> 0:2.6.2-5jpp
- Remove the tools tarball, and build xjavac from source.
- Patch xjavac to fix the classpath under libgcj too.

* Fri Jun 10 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_8fc
- Remove the tools tarball, and build xjavac from source.
- Replace classpath workaround to xjavac task and use
  xml-commons classes again (#152255).

* Thu May 26 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_7fc
- Rearrange how BC-compiled stuff is built and installed.

* Mon May 23 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_6fc
- Add alpha to the list of build architectures (#157522).
- Use absolute paths for rebuild-gcj-db.

* Thu May  5 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_5fc
- Add dependencies for %%post and %%postun scriptlets (#156901).

* Fri Apr 29 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_4fc
- BC-compile.

* Thu Apr 28 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_3fc
- Revert xjavac classpath workaround, and patch to use libgcj's
  classes instead of those in xml-commons (#152255).

* Thu Apr 21 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_2fc
- Add classpath workaround to xjavac task (#152255).

* Wed Jan 12 2005 Gary Benson <gbenson@redhat.com> 0:2.6.2-4jpp_1fc
- Reenable building of classes that require javax.swing (#130006).
- Sync with RHAPS.

* Mon Nov 15 2004 Fernando Nasser <fnasser@redhat.com>  0:2.6.2-4jpp_1rh
- Merge with upstream for 2.6.2 upgrade

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 0:2.6.2-2jpp_5fc
- Build into Fedora.

* Thu Oct 28 2004 Gary Benson <gbenson@redhat.com> 0:2.6.2-2jpp_4fc
- Bootstrap into Fedora.

* Fri Oct 1 2004 Andrew Overholt <overholt@redhat.com> 0:2.6.2-2jpp_4rh
- add coreutils BuildRequires

* Thu Sep 30 2004 Andrew Overholt <overholt@redhat.com> 0:2.6.2-2jpp_3rh
- Remove xml-commons-resolver as a Requires

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> 0:2.6.2-4jpp
- Build with ant-1.6.2
- Dropped jikes requirement, built for 1.4.2

* Wed Jun 23 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:2.6.2-3jpp
- Updated Patch #0 to fix breakage using BEA 1.4.2 SDK, new patch
  from <mwringe@redhat.com> and <vivekl@redhat.com>.

* Mon Jun 21 2004 Vivek Lakshmanan <vivekl@redhat.com> 0:2.6.2-2jpp_2rh
- Added new Source1 URL and added new %%setup to expand it under the
  expanded result of Source0.
- Updated Patch0 to fix version discrepancies.
- Added build requirement for xml-commons-apis
 
* Mon Jun 14 2004 Matt Wringe <mwringe@redhat.com> 0:2.6.2-2jpp_1rh
- Update to 2.6.2
- made patch names comformant

* Mon Mar 29 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:2.6.2-2jpp
- Rebuilt with jikes 1.18 for java 1.3.1_11

* Fri Mar 26 2004 Frank Ch. Eigler <fche@redhat.com> 0:2.6.1-1jpp_2rh
- add RHUG upgrade cleanup

* Tue Mar 23 2004 Kaj J. Niemi <kajtzu@fi.basen.net> 0:2.6.2-1jpp
- 2.6.2

* Thu Mar 11 2004 Frank Ch. Eigler <fche@redhat.com> 0:2.6.1-1jpp_1rh
- RH vacuuming
- remove jikes dependency
- add nonjikes-cast.patch

* Sun Feb 08 2004 David Walluck <david@anti-microsoft.org> 0:2.6.1-1jpp
- 2.6.1
- update Source0 URL
- now requires xml-commons-resolver

* Fri Jan  9 2004 Kaj J. Niemi <kajtzu@fi.basen.net> - 0:2.6.0-1jpp
- Update to 2.6.0
- Patch #1 (xerces-j2-manifest.patch) is unnecessary (upstream)

* Tue Oct 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.5.0-1jpp
- Update to 2.5.0.
- Clean up versionless javadoc dir symlinking, own (ghost) the symlinks.
- Mark javadocs as %%doc.

* Wed Jun  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.4.0-3jpp
- Own (ghost) %%{_javadir}/jaxp_parser_impl.jar.
- Remove alternatives in preun instead of postun.

* Mon May 12 2003 David Walluck <david@anti-microsoft.org> 0:2.4.0-2jpp
- bug #17325 fixed upstream

* Mon May 12 2003 David Walluck <david@anti-microsoft.org> 0:2.4.0-1jpp
- 2.4.0
- BuildRequires: jikes
- update for JPackage 1.5
- re-diff'ed build patch for 2.4.0
- bug #17325 handled by perl now
- scripts: s|find-jar|build-classpath| and don't test for java-functions

* Wed Mar 26 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> - 2.3.0-2jpp
- For jpackage-utils 1.5
- zapped manual, since it doesn't want to build
- as a consequence, removed uneeded dependencies

* Mon Feb 24 2003 Ville Skyttä <ville.skytta at iki.fi> - 2.3.0-1jpp
- Update to 2.3.0.
- Add a crude patch to work around invalid XML in doc sources, see
  <http://nagoya.apache.org/bugzilla/show_bug.cgi?id=17325>.
- Built with IBM's 1.3.1 SR3.

* Sat Dec 28 2002 Ville Skyttä <ville.skytta at iki.fi> - 2.2.1-2jpp
- Add upstream patch which fixes problems with Tomcat's webapps.
  <http://nagoya.apache.org/bugzilla/show_bug.cgi?id=13282>
  <http://marc.theaimsgroup.com/?l=xerces-cvs&m=103791990130308>
- Separate scripts subpackage.

* Fri Nov 15 2002 Ville Skyttä <ville.skytta at iki.fi> - 2.2.1-1jpp
- Update to 2.2.1.
- Change alternative to point to non-versioned jar.
- Don't remove alternative on upgrade.
- Fix Group tag for demo, javadoc and manual subpackages.
- Add version and constants scripts.
- Some spec file cleanup.

* Sun Oct  6 2002 Ville Skyttä <ville.skytta at iki.fi> 2.2.0-2jpp
- Fix bad permissions for main jar.

* Sun Sep 29 2002 Ville Skyttä <ville.skytta at iki.fi> 2.1.0-1jpp
- Update to 2.2.0.

* Tue Sep 10 2002 Ville Skyttä <ville.skytta at iki.fi> 2.1.0-2jpp
- Rebuild with -Dcompiler=modern, not a Jikes bug this time, but sloppy code
  that is tolerated by javac.  See <http://www-124.ibm.com/developerworks/bugs/?func=detailbug&bug_id=3218&group_id=10> for details.

* Tue Sep 10 2002 Ville Skyttä <ville.skytta at iki.fi> 2.1.0-1jpp
- 2.1.0.
- Updated description.
- Changed javadoc and manual group to Documentation.
- Spec file cleanups.

* Fri Jul 12 2002 Henri Gomez <hgomez@users.sourceforge.net> 2.0.2-4jpp
- add BuildRequires xerces-j1 and xalan-j2
- removed BuildRequires xml-commons-api since ant require jaxp_parser_impl
  which in turn require xml-commons-api ;)

* Mon Jul 01 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.2-3jpp 
- vendor, distribution, group tags
- provides jaxp_parser_impl
- dropped api jar
- renamed lone jar to %%{name}.jar
- priority bumped to 40
- fixed stylebook build (add xerces-j1 in classpath)

* Wed Jun 26 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.2-2jpp
- rebuild for missing symlinks
- use sed instead of bash 2.x extension in link area to make spec compatible with distro using bash 1.1x

* Mon Jun 24 2002 Henri Gomez <hgomez@users.sourceforge.net> 2.0.2-1jpp
- 2.0.2

* Sun Mar 10 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.1-1jpp 
- 2.0.1
- provides jaxp_parser2 virtual resource
- drop wrapper

* Sun Feb 03 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.0-1jpp 
- first JPackage release
