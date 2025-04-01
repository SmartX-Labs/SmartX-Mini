# Lab#1. Box Lab

# 0. Objective

![Final Goal](./img/final_goal.png)

Box Lab에서는 \*베어 메탈에 운영체제(OS)를 직접 설치해보고  
이 안에 가상 머신과 컨테이너를 생성한 뒤, 가상 스위치로 서로를 연결시켜봅니다.

\*베어 메탈: 하드웨어 상에 어떤 소프트웨어도 설치되어 있지 않은 상태

세부적인 구조를 보면 다음과 같습니다.

![Objective](./img/objective.png)

# 1. Theory

![VM Container](./img/vm_container.png)

> [!NOTE]
>
> - Virtual Machine
>
>   하나의 피지컬 머신 내부에서 여러개의 가상 머신을 생성하여 여러개의 독립적인 가상 머신을 구성할 수 있습니다. 각각의 가상 머신은 모두 독립적이며 개별적인 자원을 할당받습니다. 또한, 가상 머신에서는 피지컬 머신의 OS와 다른 OS를 사용자 마음대로 정해서 사용할 수 있습니다. 단순히 사용하는 측면에서 바라볼 때, 가상 머신과 피지컬 머신은 차이가 거의 없게 느껴질 수 있습니다. 그러나 가상 머신은 그만큼 container보다 무겁고 생성하는데 오래걸립니다.  
>   그러나, container와 비교했을 때, VM을 사용하는 것이 더 좋은 경우도 있습니다.
>
> 1. 특정 OS 환경에서만 작동하는 application을 실행해야 하는 경우  
>    오래 전에 개발되어 특정 OS 환경에서만 작동하는 프로그램을 실행해야 하는 경우 또는 개발자의 의도로 인해 특정 OS에서만 작동하도록 설계된 프로그램을 실행하는 경우, VM을 사용해야 합니다.
> 2. 보안이 중요한 환경  
>    VM은 container와는 다르게 VM 간에 OS를 공유하지 않기 때문에, 각각의 환경 사이의 격리 수준이 더 높습니다. 금융 데이터를 다루는 서비스와 같이 높은 수준의 보안이 필요한 경우에는 container보다는 VM이 더 적절할 수 있습니다.
>
> 이번 Lab에서는 가상 머신을 생성하기 위해 리눅스에 기본적으로 탑재되어있는 KVM Hypervisor를 사용할 것입니다.
>
> - Container
>
>   가상 머신과 비교했을 때 container가 가지는 가장 큰 다른 특징으로, 독립적인 Guest OS층이 없다는 점을 생각할 수 있습니다. Container는 가상 머신과 달리 피지컬 머신의 OS를 공유합니다. 그리고 가상 머신은 각각의 머신이 독립적이지만 Container는 그렇지 않습니다. 피지컬 머신의 OS(Host OS) 위에서 Docker Engine이 작동하고, Docker Engine 덕분에 각각의 Guest OS 없이도 격리된 환경을 구성할 수 있습니다. 이러한 구조로 인해서 가상 머신보다 훨씬 더 가볍고 빠르게 실행할 수 있으며 환경(Container)의 생성과 삭제도 비교적 간단합니다.  
>   container를 사용하면 좋은 경우는 다음과 같습니다.
>
> 1. Application의 빠른 배포가 필요한 경우
>    container를 사용하면 application의 실행 환경을 빠르게 구성하여 배포할 수 있습니다. VM과 비교했을 때 실행 시간이 짧아서 빠른 배포에 더욱 유리합니다.
> 2. 경량 application을 실행하는 경우
>    짧은 기간동안 임시 환경을 구축하여 특정 프로그램을 테스트하거나 경량 application을 실행하는 경우에는 container를 사용하는 것이 좋습니다.
>
> 이번 Lab에서는 container를 생성하기 위해서 가장 널리 쓰이는 Docker Runtime을 사용할 것입니다.

![Virtual Switch](./img/switch.png)

> [!NOTE]
>
> - Switch
>
>   스위치는 네트워크 장치들을 연결하고, 데이터 패킷을 전달하는 역할을 하는 장비입니다. 어느 네트워크 계층에서 작동하는지에 따라 L2, L3 스위치 등이 존재합니다.
>   스위치의 주요 특징은 다음과 같습니다.
>
>   1. 패킷 전달  
>      L2 스위치의 경우, MAC 주소를 기반으로 패킷을 전달합니다. 기본적인 네트워크 스위치의 역할을 합니다. L3 스위치의 경우, IP 라우팅 기능을 갖추어 라우터의 일부 기능을 수행합니다.
>
>   2. Full Duplex 통신  
>      스위치는 Full Duplex를 지원하여 송수신이 동시에 이루어집니다. 이로 인해 빠른 네트워크 통신이 가능합니다.
>
>   3. VLAN(Virtual Local Area Network) 기능 지원  
>      일부 고급 기능을 지원하는 스위치에서는 VLAN 기능을 바탕으로 논리적인 네트워크 분할을 할 수 있습니다. VLAN을 사용하면 같은 물리적 네트워크 환경 내에서도 논리적인 네트워크 구분을 할 수 있습니다.
>
> - Virtual Switch
>
>   가상 스위치는 OS안에서 실제 물리적인 스위치처럼 동작합니다. 이번 Lab에서 Open vSwitch를 통해 가상 스위치를 구성할 것이고 이 가상 스위치를 통해 가상 머신과 컨테이너를 연결할 것입니다.
>
>   Open vSwitch는 가상 서버를 위해 설계된 오픈 소스 가상 스위치 소프트웨어입니다.
>
>   소프트웨어 기반 가상 스위치는 한 VM이 다른 VM과 통신할 수 있도록 하며, 물리적 스위치를 통해 인터넷에 연결할 수 있도록 합니다. CPU의 연산 능력을 활용하여 실행되는 소프트웨어 기반 스위치는 더 유연하고 업그레이드가 용이하며, 가상화의 이점을 활용할 수 있습니다 (메모리 오버커밋, 페이지 공유 등). VM(또는 컨테이너)에는 논리적인(가상) 네트워크 인터페이스 카드(NIC)가 있으며, 가상 이더넷 포트를 통해 가상 스위치의 가상 인터페이스(포트)에 연결될 수 있습니다.

# 2. Practice

> [!TIP]
> 마우스를 코드 블럭 위에 올리게 되면 우측 상단에 복사하기 버튼이 뜹니다. 해당 버튼을 눌러 내용을 복사할 수 있습니다.해당 기능은 편의를 위해 제공됩니다. 그러나 Lab을 진행하는 과정에서 모든 것을 그대로 붙여넣기 해서는 안 됩니다. 수강생 개인마다 명령어의 일부, 또는 파일의 일부 내용을 수정해야 하기 때문에, 문서의 내용을 꼼꼼히 살펴보고 수정해야 하는 부분은 꼭 수정해주시기 바랍니다.  
> ![copy button](img/copy.png)

> [!IMPORTANT]
> 사용하는 NUC과 가상 머신(VM), 그리고 container의 IP가 적힌 종이를 참고하여 Lab을 진행해주시길 바랍니다.  
> **NUC**은 `Next Unit of Computing`의 약자로, Intel에서 개발한 초소형 컴퓨터입니다. 우리는 NUC을 이용하여 lab을 진행합니다.  
> 앞으로 NUC이라는 용어는 여러분이 사용하는 컴퓨터를 지칭하는 의미로 사용될 것입니다.
>
> 1. NUC IP: NUC이라고 적힌 부분의 IP를 사용합니다.
> 2. VM IP: Extra라고 적힌 부분의 IP를 사용합니다.
> 3. Container IP: 이번 Lab에 한정하여 PI라고 적힌 부분의 IP를 사용합니다.

## 2-1. NUC: OS Installation and Network Configuration

> [!NOTE]
> 수강생들 중, Playground Lab에서 OS를 설치한 경우에는 OS Installation 부분을 생략합니다.

Lab에서 사용할 Host OS는 다음과 같습니다. 제공받은 설치 USB를 사용하여 OS를 설치하면 됩니다.  
OS : Ubuntu Desktop 22.04 LTS(64bit)  
참고: Download Site - <https://releases.ubuntu.com/22.04/>

### 2-1-1. Boot Configuration

1. NUC의 전원이 꺼진 상태에서 OS 설치를 위한 USB를 NUC에 연결한 뒤에, NUC의 전원을 켭니다.
2. 부팅이 시작되면 F10 키를 눌러서 Boot device를 선택하는 화면에 진입합니다.
3. Boot device 리스트에서 USB에 해당하는 것을 선택합니다. (ex. UEFI: SanDisk ...)
4. Try or install ubuntu를 선택하여 실행합니다.

### 2-1-2. Installation

1. Install Ubuntu를 선택합니다. (Try Ubuntu X) 언어는 English로 진행해야합니다.
2. Keyboard layout 설정 단계에서도 "English(US)"로 설정합니다.
3. Wireless 탭이 뜨면, "I don't want to connect to a Wi-Fi network right now"를 선택하고 넘어갑니다.
4. Updates and other software 단계에서 "What apps would you like to install to start with?" 영역에서 "Minimal installation"을 선택하고 다음 단계로 넘어갑니다.
5. Installation type 단계에서 "Erase disk and install Ubuntu"를 선택하고 "Install now" 버튼을 누릅니다.
6. Write the changes to disks? 창이 뜨면 Continue를 눌러 계속 진행합니다.
7. Location 설정 화면에서 "Seoul"을 선택합니다.
8. User 정보와 Computer 정보를 입력하는 "Who are you" 단계에 진입했다면 다음과 같이 설정합니다.

   - Your name: gist
   - Your computer's name: nuc<NUC IP주소의 마지막 3자리 숫자>  
     -> ex. XXX.XXX.XXX.109의 경우, nuc109
   - Pick a username: gist
   - 비밀번호의 경우, 조교의 안내에 따라 설정을 진행합니다.

9. 모든 설정이 완료되었다면 버튼을 눌러 최종 설치를 진행합니다.
10. 설치가 완료되면, "Restart now" 버튼을 눌러 NUC을 다시 시작합니다.
11. 재시작 과정에서 "Please remove the installation medium, then press ENTER" 메세지가 보이면, 설치 USB를 제거한 뒤에 ENTER 키를 누릅니다.

  <details>
    <summary>에러 발생 시 참고(정상 설치가 되었다면 이 부분은 생략합니다.)</summary>

- Select ‘Something else’
- On /dev/sda or /dev/nvme0n1

- (UEFI), add 512MB EFI partition
- Add empty partition with 20GB (20480MB) (Select ‘do not use the partition’)
- Add Etc4 partition on leave memory

- Select Boot loader

  - BIOS: Ext4 partition
  - UEFI: EFI partition

- LVM 관련 오류 발생 시

  1. 뒤로 이동하여, 첫 Installation type 화면으로 이동
  2. select Erase disk

     - choose none in advance.

  3. 시간대 선택 화면까지 진행
  4. 여기서 뒤로 돌아가, 다시 첫 Installation type 화면으로 이동
  5. Something else 선택하여 정상 진행
  </details>

### 2-1-3. Basic Network Configuration after OS Installation

> [!CAUTION]  
> <b>⚠️ (중요. 로그인 뒤에 Ubuntu를 업데이트할 것인지 묻는 창이 뜬다면 반드시 Don't Upgrade를 선택해야합니다!) ⚠️</b>

- 로그인 화면이 보이면, 계정 정보를 입력하여 로그인합니다. 이제부터는 초기 네트워크 설정을 진행할 것입니다.
- ‘Temporary’ Network Configuration using GUI

  ![Network Configuration](./img/network_configuration.png)

- 화면 우측 상단을 클릭하여 "Ethernet(enp88s0 or enp89s0) Connected" 부분을 선택합니다. 그리고 "Wired Settings"를 누릅니다.

  <p align="center">
    <img src="./img/network_setting1.png" />
  </p><br>

- Ethernet 부분에서 오른쪽에 있는 톱니바퀴 아이콘을 눌러 설정 탭에 들어갑니다.
  <p align="center">
    <img src="./img/network_setting2.png" />
  </p><br>

- IPv4 탭으로 전환하고, 각자 할당받은 네트워크 정보를 입력합니다.

  - IPv4 Method: Manual
  - Address: 할당받은 NUC의 IP 주소 (IP가 적힌 종이를 참고합니다.)
  - Netmask와 Gateway, DNS 정보도 입력합니다. (조교의 안내를 바탕으로 설정합니다.)
  <p align="center">
    <img src="./img/network_setting3.png" />
  </p><br>

## 2-2. NUC: Network Configuration Using Virtual Switch

> [!CAUTION]  
> <b>⚠️ (중요. 로그인 뒤에 Ubuntu를 업데이트할 것인지 묻는 창이 뜬다면 반드시 Don't Upgrade를 선택해야합니다!) ⚠️</b>

1. apt Update & Upgrade

   - Lab에서는 패키지 관리자인 apt를 사용합니다. 앞으로 사용할 패키지들을 설치하기 위해 패키지 목록을 최신으로 업데이트하고, 업데이트 가능한 패키지를 실제로 업데이트합니다.
   - 명령어를 실행하기 위해 터미널을 엽니다. 터미널은 화면 좌하단에 위치한 앱 리스트 아이콘을 누르고, 리스트에서 터미널 아이콘을 눌러 실행할 수 있습니다.

   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. Install vim text editor

   - 앞으로 vim editor를 사용하여 파일의 내용을 수정하겠습니다. vim을 설치합니다.

   ```bash
   sudo apt install vim
   ```

3. Install net-tools & ifupdown

   - network 관련 유틸리티를 실행하기 위해 net-tools와 ifupdown을 설치합니다. 그리고 `ifconfig -a` 명령어를 통해 network interface 정보를 확인합니다.

   ```bash
   sudo apt install -y net-tools ifupdown
   ifconfig -a
   ```

   ![Network Configuration](./img/ifconfig.png)

4. Install openvswitch-switch & make br0 bridge

   - 가상 네트워크 스위치를 만들기 위해 openvswitch-switch를 설치합니다. 그리고 br0이라는 OVS(Open vSwitch) 브릿지를 만듭니다. OVS 브릿지는 여러 가상 네트워크 인터페이스를 연결하는 가상의 스위치 역할을 합니다. 최종적으로 OVS의 설정 상태를 확인합니다.

   ```bash
   sudo apt -y install openvswitch-switch
   sudo ovs-vsctl add-br br0
   sudo ovs-vsctl show
   ```

   ![Ovs Vsctl Show](./img/ovs_vsctl_show.png)

5. Disable netplan

   - Open vSwitch(OVS)를 기반으로 수동 네트워크 관리 방법을 사용하기 위해서 systemd-networkd 및 Netplan을 비활성화하고 제거합니다.

   ```bash
   sudo systemctl stop systemd-networkd.socket systemd-networkd networkd-dispatcher systemd-networkd-wait-online
   sudo systemctl disable systemd-networkd.socket systemd-networkd networkd-dispatcher systemd-networkd-wait-online
   sudo systemctl mask systemd-networkd.socket systemd-networkd networkd-dispatcher systemd-networkd-wait-online
   sudo apt-get --assume-yes purge nplan netplan.io
   ```

   - DNS configuration

   ```bash
   sudo vim /etc/systemd/resolved.conf
   ```

   파일의 내용 중, DNS 왼편에 있는 주석표시 (#) 를 제거해주고 DNS 주소를 명시합니다.  
   (참고: 실습 환경에 따라 `DNS`의 값이 달라질 수 있습니다.)

   > …
   >
   > DNS=203.237.32.100 203.237.32.101
   >
   > …

   - Network interface configuration

   /etc/network/interfaces 파일을 엽니다.

   ```bash
   sudo vim /etc/network/interfaces
   ```

   `vport_vFunction`을 TAP 인터페이스로 설정하고 VM에 연결합니다.

> [!NOTE]
> TAP 인터페이스는 VM과 Host 사이의 네트워크 통신이 가능하도록 합니다. TAP 인터페이스를 이용하면, VM이 마치 물리적 네트워크 인터페이스를 가진 것처럼 동작하게 만들 수 있으며, 네트워크 브리지와 결합하여 외부의 네트워크와 통신할 수 있도록 합니다.
>
> TAP 인터페이스를 `br0`과 같은 브리지 네트워크에 연결하여 bridge 네트워크를 구성하면 VM과 Host가 같은 서브넷에서 동작하게 만들 수 있습니다. 그렇게 되면, 해당 VM이 물리적으로 네트워크에 연결된 것처럼 동작하도록 만들 수 있습니다.

> [!CAUTION]  
> **!!!들여쓰기는 Tab 한번입니다!!!**  
> `<your nuc ip>`에 현재 nuc의 ip와 `<gateway ip>`에 gateway ip를 입력해주시기 바랍니다. (이때 괄호는 제외하고 입력해야 합니다.)

> [!CAUTION]
> ⚠️ **주의!** ⚠️  
> <b>NUC에 이더넷 포트가 두 개 있는 경우 `eno1`이라는 인터페이스가 없습니다. `ifconfig` 명령으로 네트워크에 연결된 인터페이스(`enp88s0` 또는 `enp89s0`)를 확인합니다. (예를 들어, 터미널에 `ifconfig -a` 명령어를 입력하고 RX 및 TX 패킷이 0이 아닌 인터페이스를 선택합니다.) 그리고 아래 텍스트의 `eno1`을 모두 `enp88s0` 또는 `enp89s0`으로 변경합니다.</b>

아래의 내용을 추가합니다.(참고: 실습 환경에 따라 `address`, `netmask`, `gateway`, `dns-nameservers`의 값이 달라질 수 있습니다.)

```text
auto lo
iface lo inet loopback

auto br0
iface br0 inet static
    address <your nuc ip>
    netmask 255.255.255.0
    gateway <gateway ip>
    dns-nameservers 203.237.32.100

auto eno1
iface eno1 inet manual

auto vport_vFunction
iface vport_vFunction inet manual
    pre-up ip tuntap add vport_vFunction mode tap
    up ip link set dev vport_vFunction up
    post-down ip link del dev vport_vFunction
```

> [!NOTE]
> ⚠️ **위의 내용에 대한 설명입니다. 따로 파일에 입력하지 않아도 됩니다.** ⚠️  
> (참고: 실습 환경에 따라 `address`, `netmask`, `gateway`, `dns-nameservers`의 값이 달라질 수 있습니다.)
>
> - Loopback 인터페이스 설정
>   Loopback 인터페이스를 자동으로 활성화하고, loopback(자기 자신을 참조하는 가상 네트워크 인터페이스)으로 설정합니다.
>
>   ```text
>   auto lo
>   iface lo inet loopback
>   ```
>
> - Bridge 네트워크 인터페이스 설정
>   br0라는 가상 브릿지(Bridge) 네트워크 인터페이스를 생성하고 부팅 시에 자동으로 활성화되도록 합니다. 정적 IP를 사용하도록 명시하고, IP 주소 등의 네트워크 설정 값을 입력합니다.
>
>   ```text
>   auto br0
>   iface br0 inet static
>     address <your nuc ip>
>     netmask 255.255.255.0
>     gateway <gateway ip>
>     dns-nameservers 203.237.32.100
>   ```
>
> - 물리적 인터페이스 설정
>   eno1(물리적 이더넷 인터페이스)을 부팅 시 자동으로 활성화합니다. eno1에게는 직접 IP 주소를 할당하지 않을 것이고, br0에 속하는 구성원으로 다룰 것입니다.
>
>   ```text
>   auto eno1
>   iface eno1 inet manual
>   ```
>
> - TAP 인터페이스 생성
>   vport_vFunction이라는 가상 TAP(Tunnel Access Point) 인터페이스를 생성하고 부팅 시 활성화되도록 합니다. 수동으로 네트워크를 설정해야 하는 수동(manual) 모드로 지정합니다.
>
>   ```text
>   auto vport_vFunction
>   iface vport_vFunction inet manual
>     pre-up ip tuntap add vport_vFunction mode tap
>     up ip link set dev vport_vFunction up
>     post-down ip link del dev vport_vFunction
>   ```

> [!CAUTION]
> ⚠️ **주의!** ⚠️  
> <b> 만약 NUC에 2개의 ethernet port가 있다면, `eno1` interface가 없습니다. 그러므로 하단의 block에서 `eno1`을 위에서 선택한 interface 중 하나로 변경해주시기 바랍니다.(`enp88s0` 또는 `enp89s0` 중에서 현재 사용중인 것을 선택하면 됩니다.)</b>

```bash
sudo systemctl restart systemd-resolved.service
sudo ifup eno1  #change this if you are using two-port NUC
```

전체 interface를 다시 시작합니다.

```bash
sudo systemctl unmask networking
sudo systemctl enable networking
sudo systemctl restart networking
```

vport_vFunction을 연결한 가상 머신(VM)을 만들겠습니다. 이 TAP(vport_vFunction)은 VM의 NIC(네트워크 인터페이스 카드)라고 생각하면 됩니다.

'br0'에 포트 'eno1' 및 'vport_vFunction'을 추가합니다.

> [!CAUTION]
> ⚠️ **주의!** ⚠️  
> <b> 만약 NUC에 2개의 ethernet port가 있다면, `eno1` interface가 없습니다. 그러므로 하단의 block에서 `eno1`을 위에서 선택한 interface 중 하나로 변경해야합니다.(`enp88s0` 또는 `enp89s0` 중에서 현재 사용 중인 것을 선택합니다.)</b>

```bash
sudo ovs-vsctl add-port br0 eno1   #change this if you are using two-port NUC
sudo ovs-vsctl add-port br0 vport_vFunction
sudo ovs-vsctl show
```

지금까지의 설정 구성입니다.

![vport_vFunction](./img/vport_vFunction.png)

`sudo ovs-vsctl show` 명령어 실행 후, Bridge `br0` 아래에 `vport_vFunction`과 사용중인 네트워크 인터페이스 (`eno1` 또는 `enp88s0` 또는 `enp89s0` 중 1개)가 등록되어 있으면 성공적으로 설정이 된 것입니다.

전체 interface를 다시 시작합니다.

```bash
sudo systemctl unmask networking
sudo systemctl enable networking
sudo systemctl restart networking
```

## 2-3. NUC: Making VM with KVM

- Install required packages to set up and manage KVM

  KVM을 설정하고 관리하기 위한 dependency를 설치하고, VM 안에서 사용할 Ubuntu 22.04.5 image를 다운받습니다.

  - qemu-kvm: QEMU(Quick Emulator) 기반으로 KVM(커널 기반 가상화)을 지원합니다.
  - libvirt-daemon-system: libvirtd 데몬을 실행하여 가상 머신을 관리할 수 있도록 지원합니다.
  - libvirt-clients: VM 관리 명령어를 제공합니다.
  - bridge-utils: VM이 Host machine과 동일한 네트워크에서 동작할 수 있도록 설정하기 위해 사용합니다.

  ```bash
  sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
  # upgrade KVM
  # qemu is open-source emulator

  wget https://ftp.lanet.kr/ubuntu-releases/22.04.5/ubuntu-22.04.5-live-server-amd64.iso
  ```

- Prepare for Ubuntu VM

  VM에서 사용할 가상 디스크 image를 만들기 위해, 아래의 명령어를 실행합니다.

  ```bash
  sudo qemu-img create vFunction22.img -f qcow2 10G
  ```

  아래의 명령어를 입력하여 VM을 백그라운드 모드로 실행합니다.

  **띄어쓰기 주의하기**

  ```bash
  sudo kvm -m 2048 -name tt \
  -smp cpus=4,maxcpus=4 \
  -device virtio-net-pci,netdev=net0 \
  -netdev tap,id=net0,ifname=vport_vFunction,script=no \
  -boot d vFunction22.img \
  -cdrom ubuntu-22.04.5-live-server-amd64.iso \
  -vnc :5 -daemonize \
  -monitor telnet:127.0.0.1:3010,server,nowait,ipv4 \
  -cpu host
  ```

- Install Ubuntu VM

  VNC viewer를 설치하여 VM의 작동을 확인합니다.

  ```bash
  sudo apt install tigervnc-viewer
  ```

  VM을 실행합니다.

  ```bash
  vncviewer localhost:5
  ```

  이렇게 viewer 안에 Ubuntu 설치 화면이 보일 것입니다.

  ![Install Ubuntu](./img/install_ubuntu.png)

  설치 단계 (Enter키와 방향키를 사용하여 설치를 진행합니다.)

  1. 언어 설정 화면에서 English로 설정합니다.
  2. "Keyboard configuration" 화면에서는 모든 부분을 English(US)로 설정합니다.
  3. "Choose the type of installation" 화면에서는 "Ubuntu Server" 부분에 (X) 표시가 되어있는지 확인하고 Done을 누릅니다.
  4. "Network configuration" 화면에 진입하여 아래와 같이 "Edit IPv4"를 눌러줍니다.
     ![Ubuntu Network](./img/ubuntu_network.png)
  5. 아래 내용을 참고하여 설정해줍니다.(VM IP로 종이에 적힌 Extra IP 주소를 사용합니다.)

     > IPv4 Method → Manual
     >
     > subnet: 172.29.0.0/24  
     > Address: < VM IP(Extra IP) >  
     > Gateway: 172.29.0.254  
     > Name Servers: 203.237.32.100

     ⚠️ Search domains에는 아무것도 적지 않습니다! ⚠️

     그리고 위의 `< VM IP(Extra IP) >` 작성 시에 **괄호는 지우고** 172.29.0.X의 형식으로 작성해야 합니다.

  6. "Proxy configuration" 화면에서는 아무것도 입력하지 않고 넘어갑니다.
  7. "Ubuntu archive mirror configuration" 화면에서도 Done을 눌러 넘어갑니다.
  8. ⚠️ **(중요)** "Installer update available" 화면에서는 "Continue without updating"을 선택합니다.
  9. "Guided storage configuration", "Storage configuration" 화면에서도 내용을 수정하지 않고 Done을 계속 눌러서 넘어갑니다. 마지막에 "Confirm destructive action" 창이 뜨면 Continue를 눌러 넘어갑니다.
  10. "Profile configuration" 화면에서는 아래와 같이 입력합니다.
      - Your name: vm
      - Your servers name: vm<VM IP주소의 마지막 3자리 숫자>  
        -> ex. XXX.XXX.XXX.179의 경우, vm179
      - Pick a username: vm
      - 비밀번호의 경우, NUC의 비밀번호와 동일하게 설정합니다.
  11. "Upgrade to Ubuntu Pro" 화면이 나오면 "Skip for now"에 (X) 표시가 되어있는지 확인하고 넘어갑니다.
  12. "SSH configuration" 화면이 나오면 아무것도 수정하지 않고 Done을 눌러 넘어갑니다.
  13. "Featured server snaps" 화면이 나오면 아무것도 선택하지 않고 Done을 눌러 넘어갑니다.
  14. 설치 진행 상황을 볼 수 있는 화면이 나옵니다.
  15. 설치가 완료되어 아래와 같이 화면이 나오면 `Reboot Now` 버튼이 보일 것입니다. 그러나, ⚠️ **버튼을 누르지 않고 아래의 내용을 따라주시길 바랍니다**.
      ![Ubuntu Network](./img/ubuntu-installation-done.png)

- Installation Completed

  VM 내에서 ubuntu의 설치가 완료되어 `Reboot Now` 버튼이 보이면, ⚠️ **Host OS의 터미널을 새로 하나 생성한 뒤에** 아래의 명령어를 입력하여 VM을 종료합니다.

> [!TIP]
> 새로운 터미널은 터미널 창의 좌상단에 위치한 `+` 버튼을 누르면 생성할 수 있습니다.

```bash
sudo killall -9 kvm
```

아래의 명령어를 입력하여 VM을 다시 실행합니다.

```bash
sudo kvm -m 1024 -name tt \
-smp cpus=2,maxcpus=2 \
-device virtio-net-pci,netdev=net0 \
-netdev tap,id=net0,ifname=vport_vFunction,script=no \
-boot d vFunction22.img
```

## 2-4. OVS connects with KVM

- Check configuration(In NUC)  
  지금까지 설정한 네트워크 인터페이스의 상태를 확인해보기 위해 NUC에서 아래의 명령어를 실행합니다.

  ```bash
  sudo ovs-vsctl show
  ```

## 2-5. Install docker

Docker 리포지토리 추가를 위해 apt를 HTTPS 지원 가능하도록 설정하고, 필요한 패키지를 설치합니다.

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```

Docker 공식 GPG Key를 추가합니다.

```bash
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

apt source list에 Docker 저장소를 추가합니다.

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Docker를 설치합니다.

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

Docker daemon을 설정합니다.

```bash
sudo mkdir -p /etc/docker

cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF
```

/etc/systemd/system/docker.service.d 디렉터리를 생성합니다.

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo systemctl daemon-reload
sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl start docker.socket
```

## 2-7. Check docker installation

아래의 명령어를 실행하여 docker의 실행을 확인해봅니다.

```bash
sudo docker run hello-world
```

잘 작동한다면 아래와 같은 내용이 출력됩니다.

![1](./img/1.png)

## 2-8. Make Container

c1이라는 이름의 container를 생성해봅니다. 이 container는 ubuntu:22.04 이미지를 바탕으로 생성되며, 최초 실행 시, /bin/bash가 실행되도록 합니다. `--net=none` 옵션을 사용하여 container가 네트워크에 연결되지 않도록 합니다.

```bash
sudo docker run -it --net=none --name c1 ubuntu:22.04 /bin/bash
```

ctrl + p, q를 누르면 container를 종료하지 않고 container 밖으로 나올 수 있습니다.

> [!TIP]
> docker attach [container_name]:  
> 위의 명령어를 입력하면 ctrl + p, q를 사용하여 detach 했던 container 안으로 다시 들어갈 수 있습니다.

## 2-9. Connect docker container

**도커 외부에서**, 즉 Host machine에서 하단의 명령어를 실행합니다.  
이 명령어는 **Open vSwitch(OVS)**를 사용하여 Docker container(c1)에 특정 네트워크 인터페이스(veno1)를 추가하고, 이를 가상 브리지(br0)에 연결합니다.

```bash
sudo docker start c1
sudo ovs-docker add-port br0 veno1 c1 --ipaddress=<docker_container_IP>/24 --gateway=<gateway_IP>
# please type gateway IP and docker container IP.
```

> [!WARNING]
> ⚠️ 이번 Lab에 한하여 docker_container_IP는 종이에 적힌 **PI의 IP를 사용**합니다. ⚠️  
> 위의 --ipaddress=<docker_container_IP>/24 --gateway=<gateway_IP> 작성 시에 `<>`은 빼고, 172.29.0.X의 형식으로 작성해주시기 바랍니다.  
> 예를 들어, --ipaddress=172.29.0.X/24 --gateway=172.29.0.254

> [!NOTE]  
> <b> ⚠️ 아무 문제가 없었다면, 이 부분(Note block)은 생략합니다. ⚠️  
> 만약, `sudo ovs-docker add-port br0 veno1 c1 --ipaddress=<docker_container_IP>/24 --gateway=<gateway_IP>` 명령어를 실행하는 과정에서 오타나 실수가 있었다면 `sudo ovs-docker del-port br0 veno1 c1` 명령어를 실행하고 다시 `sudo ovs-docker add-port br0 veno1 c1 --ipaddress=<docker_container_IP>/24 --gateway=<gateway_IP>`를 실행합니다.</b>

Docker container 안으로 진입합니다.

```bash
sudo docker attach c1
```

container 안에서 아래의 명령어를 실행하여 네트워크 관련 도구들을 설치합니다.

```bash
apt update
apt install -y net-tools
apt install -y iputils-ping
```

## 2-10. Check connectivity: VM & Container

ping 명령어를 사용하여 Docker container 내부에서 VM으로 통신이 잘 이루어지는지 확인합니다.

```bash
ping <VM IP(Extra IP)>
# please type this command in the container.
```

예를 들어, ping 172.29.0.X

마찬가지로, VM 내부에서도 아래의 명령어를 실행하여 네트워크 관련 도구들을 설치하고 container로 통신이 잘 되는지 확인합니다.

```bash
sudo apt update
sudo apt install -y net-tools
sudo apt install -y iputils-ping
```

```bash
ping <Docker container IP address>
# please type this command in the VM.
```

**최종적으로, container와 VM의 네트워크가 연결되었음을 확인할 수 있습니다.**

# 3. Lab Summary

이 Lab의 목표는 가상 스위치를 생성해보고, VM과 Container 사이의 통신을 가상 스위치를 통해 실행해보는 것이었습니다.  
여러분은 하나의 NUC 안에 직접 VM과 Docker container를 생성하고, 네트워크 인터페이스 설정을 통해 두 요소 간의 통신이 가능하도록 만들었습니다.

## (Recall) 가상화 기술이 왜 필요한가?

VM, container와 같은 가상화 기술은 컴퓨팅 자원을 효율적으로 사용하고, 개발 및 운영을 유연하게 하기 위해 필요합니다. 가상화 기술을 사용하여 다양한 프로세스가 격리된 환경에서 작동하도록 만들 수 있습니다. 이러한 점을 바탕으로, 가상화 기술을 사용하면 다양한 환경(온프레미스, 클라우드)에서 프로그램이 원활하게 실행될 수 있는 것입니다.

## 주요 과정 요약

1. NUC의 네트워크 설정
2. 가상 스위치 설정
3. VM 생성 및 네트워크 설정
4. Docker container 생성 및 VM과의 통신 확인

## Appendix. Keep Docker network configuration

Whenever NUC is rebooted, network configuration of Docker container is initialized by executing commands in `rc.local` file.
