%define _libexecdir /usr/libexec
%define debugcflags %nil

#debuginfo not supported with Go
%global debug_package %{nil}
%global import_path github.com/opencontainers/runc
%global go_dir  %{_libdir}/go
%define gosrc %{go_dir}/src/%{import_path}
%define provider github
%define provider_tld com
%define project opencontainers
%define	shortcommit 4dc5990
%define pre rc4

Name:           runc
Version:        1.0.0
# drop me on release
Epoch:		2
Release:        %{?pre:0.%{pre}.}1
Summary:        CLI tool for spawning and running containers
License:        ASL 2.0
Group:		System/Base
URL:            http://www.docker.com
Source0:        https://%{import_path}/archive/v%{version}%{?pre:-%{pre}}.tar.gz
BuildRequires:  glibc-static-devel

BuildRequires:  golang
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:	pkgconfig(libseccomp)

BuildRequires:  go-md2man
BuildRequires:  pkgconfig(systemd)
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	btrfs-devel
Requires:       systemd

# need xz to work with ubuntu images
# https://bugzilla.redhat.com/show_bug.cgi?id=1045220
Requires:       xz
# https://bugzilla.redhat.com/show_bug.cgi?id=1034919
# No longer needed in Fedora because of libcontainer
Requires:       libcgroup
Requires:	e2fsprogs
Requires:	iptables

%description
runc is a CLI tool for spawning and running containers
according to the OCI specification.

%prep
%setup -qn %{name}-%{version}%{?pre:-%{pre}}
%apply_patches


%build
mkdir -p GOPATH
pushd GOPATH
    mkdir -p src/%{provider}.%{provider_tld}/%{project}
    ln -s $(dirs +1 -l) src/%{import_path}
popd
pushd GOPATH/src/%{import_path}
export GOPATH=%{gopath}:$(pwd)/GOPATH

mkdir -p bfd
ln -s %{_bindir}/ld.bfd bfd/ld
export PATH=$PWD/bfd:$PATH
%make BUILDTAGS=""

%install
# install binary
install -d %{buildroot}%{_sbindir}
install -p -m 755 runc %{buildroot}%{_sbindir}/
ln -s runc %{buildroot}%{_sbindir}/docker-runc

%files
%{_sbindir}/runc
%{_sbindir}/docker-runc
