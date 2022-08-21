# wquery
### 简介
&emsp;&emsp;这是一个简单的http客户端，提供了武理（本科可查，研究生院没有试过）寝室电费和个人网费查询的功能，查询结果会默认输出在终端，也可以通过在配置文件[user-info.ini]中配置[go-cqhttp][cqhttp]并开启QQ通知功能来将输出发送到指定的账号或者群聊。

### 运行
- **运行main.py启动程序**
> - 安装第三方依赖库
> ```shell
> pip install -r requirements.txt
> ```
> - python启动main.py
> ```shell
> python src/main.py
> ```
- **build.py编译可执行文件启动**
> - 执行build.py脚本
> ```shell
> python build.py
> ```
> - 运行生成的可执行程序
> ```shell
> ./dist/wquery/wquery
> dist/wquery/wquery.exe
> ```

### 运行过程
&emsp;&emsp;项目将用户查询变量存储在配置文件[user-info.ini]中，程序启动时会将配置项载入。程序向服务器请求登录页面，将登录页中生成的辅助加密序列与配置中的账号密码组合，通过登录页中提交表单时使用的加密函数（调用js）加密，最终将参数装入请求体向服务端发起登录请求，拿到Cookie，同时将会话对象序列化后存储到本地，以便下次查询跳过获取Cookie的步骤。然后程序将所有查询任务加入到任务队列，依次执行，将所有的查询结果封装成一个数据对象，最后通过数据对象将数据集输出到终端并发送到QQ。

### 配置文件
- **service-switch**  
  这个分区是查询服务的开关，当配置项值为true，则代表程序会执行这个查询任务，否则不会将该任务加入到任务队列。
> - electricity-bill： 查询寝室电费服务
> - net-bill： 查询个人网费服务
- **room**  
  这个分区存放寝室相关的信息，目前主要用来在电费查询中获取寝室电表id。
> - building： 寝室所在的宿舍楼（此处对照[build-info.json](build-info.json)填写宿舍楼对应的编号）
> - floor： 寝室所在楼层
> - room： 寝室门牌号
- **zhlgd**  
  这个分区存放智慧理工大登录信息，用于获取通用Cookie。
> - username： 智慧理工大账号
> - password： 智慧理工大密码
- **cqhttp**  
  这个分区存放[go-cqhttp][cqhttp]配置信息。当QQ通知开启时，会根据配置信息向目标cqhttp发起请求。
> - base_url： [go-cqhttp][cqhttp]服务地址。数据输出时，按照[go-cqhttp文档](https://docs.go-cqhttp.org/api/)对该地址发出对应的请求来实现QQ通知。
- **qq**  
  这个分区存放通知目标的QQ信息。
> - switch： 是否启用QQ通知，如果开启，在数据输出时会使用cqhttp中配置的接口来通知目标。如果此配置项开启，则必须先配置cqhttp分区的base_url。
> - userid： 如果switch开启，在查询完成后会将结果发送到这里指定的QQ号上。
> - groupid： 同上，这里是发送到Q群
- **system**  
  程序运行时会用到的参数，无需手动修改
> - user-info-hash： 此项存放上一次程序成功启动后，由智慧理工大账号和密码hash后的值。程序在启动时会在读取账号密码后生成新的hash值，并与此项进行比对。如果相同，则说明用户登录信息没有变动，那么就可以直接尝试加载本地存储的会话信息，否则，直接根据读入的信息尝试重新获取Cookie。

### 注意
&emsp;&emsp;这个项目仅供学习、娱乐使用，请勿对项目中列举出的接口进行扫描、sql注入、ddos等恶意行为。

[cqhttp]: https://github.com/Mrs4s/go-cqhttp
[user-info.ini]: user-info.ini