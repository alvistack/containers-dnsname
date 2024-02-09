# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: containernetworking-dnsname
Epoch: 100
Version: 1.3.1
Release: 1%{?dist}
Summary: CNI plugin to provide name resolution for containers
License: Apache-2.0
URL: https://github.com/containers/dnsname/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.23
BuildRequires: glibc-static
Requires: containernetworking-plugins
Requires: dnsmasq

%description
This CNI plugin sets up the use of dnsmasq on a given CNI network so
that Pods can resolve each other by name. When configured, the pod and
its IP address are added to a network specific hosts file that dnsmasq
reads in. Similarly, when a pod is removed from the network, it will
remove the entry from the hosts file. Each CNI network will have its own
dnsmasq instance. The dnsname plugin was specifically designed for the
Podman container engine.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
        go build \
            -mod vendor -buildmode pie -v \
            -ldflags "-s -w -X main.gitCommit=18822f9a4fb35d1349eb256f4cd2bfd372474d84" \
            -o ./bin/dnsname github.com/containers/dnsname/plugins/meta/dnsname

%install
install -Dpm755 -d %{buildroot}/opt/cni/bin
install -Dpm755 -t %{buildroot}/opt/cni/bin bin/dnsname

%files
%license LICENSE
%dir /opt/cni
%dir /opt/cni/bin
/opt/cni/bin/*

%changelog
