from manim import *
from manim.opengl import *

BACKGROUND="#2B3A42"

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"


# <a href="https://www.flaticon.com/free-icons/person" title="person icons">Person icons created by photo3idea_studio - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/person" title="person icons">Person icons created by photo3idea_studio - Flaticon</a>

class APacket(Scene):

    # stack related tasks
    def create_stack(self, length=5,height=0.5,color=OBJ_A):
        stack = VGroup()
        for i in range(length):
            r_color = OBJ_A
            height = height
            rect = Rectangle(color=r_color, fill_opacity=0.2, width=3, height=height,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(stack, DOWN, buff=0)
            stack.add(rect)
        stack.move_to(ORIGIN)
        return stack


    def construct(self):

        self.camera.background_color = BACKGROUND

        subject = Text("分层")

        self.play(FadeIn(subject))
        self.wait()
        self.play(FadeOut(subject))

        man = ImageMobject("./resource/man.png").scale(0.5).shift(LEFT*3)
        woman = ImageMobject("./resource/girl.png").scale(0.5).shift(RIGHT*3)
        self.play(
            FadeIn(man),
            FadeIn(woman),
        )

        comm_start = man.get_edge_center(RIGHT)
        comm_end = woman.get_edge_center(LEFT)
        path = Line(start=comm_start, end = comm_end)

        self.play(GrowFromPoint(path, comm_start))

        packet = Dot(radius=0.2).set_color(OBJ_A)
        packets = VMobject()
        self.add(packet, packets)
        packets.add_updater(lambda x: x.become(
            Line(comm_start, packet.get_center()).set_color(OBJ_A)
        ))
        self.play(MoveAlongPath(packet, path),rate_func=linear)
        self.wait()

        bad = ImageMobject("./resource/bad.png").scale(0.3).move_to(path)
        self.play(Wiggle(bad))
        self.play(FadeOut(bad))

        self.remove(man, woman, path, packet, packets)

        protocol_msg = "发送的消息,一定回复\n如果没有回复\n1分钟后再发送一条\n直到收到答复为止"
        protocol = Text(protocol_msg, color=WORD_A)

        self.play(Create(protocol), run_time=3)

        self.play(FadeOut(protocol))
        proto_name = Text("嘴层", color=WORD_B).scale(2)
        self.play(FadeIn(proto_name))

        tcpip = self.create_stack(5, height=1)

        self.play(proto_name.animate.scale(0.5).scale(0.8).move_to(tcpip[0]))

        self.play(FadeIn(tcpip))

        glevel = VGroup()
        levels = ["应用层", "运输层","网络层",  "物理链路层",]
        for i in range(len(levels)):
            glevel.add(Text(levels[i], color=WORD_A).scale(0.8).move_to(tcpip[i+1]))

        self.play(FadeIn(glevel))

        customize_proto = VGroup(glevel, tcpip, proto_name)
        self.play(FadeOut(customize_proto))

        self.wait()

class PacketMovement(Scene):
    
    
    def construct(self):
        # 设置车厢的尺寸
        carriage_height = 2.0
        carriage_width = 4.0
        
        # 设置车头的尺寸
        cab_height = 1.5
        cab_width = 1.25
        
        # 创建车厢的矩形
        carriage = Rectangle(height=carriage_height, width=carriage_width)
        carriage.set_fill(OBJ_B, opacity=0.3) # 设置填充颜色和不透明度
        
        # 创建车头的矩形
        cab = Rectangle(height=cab_height, width=cab_width)
        cab.set_fill(OBJ_C, opacity=0.3) # 设置填充颜色和不透明度
        
        #将车头放置在车厢旁边
        cab.next_to(carriage, RIGHT, buff=0)
        
        # 对整个货车进行组合
        truck = VGroup(carriage, cab).scale(0.5)
        
        # 将货车放置在屏幕中心
        truck.move_to(ORIGIN)
        
        # 将货车添加到场景中
        self.add(truck)

        path = Line(LEFT*9, RIGHT*9)
        packets = VMobject()
        self.add(path, packets)
        packets.add_updater(lambda x: x.become(
            Line(LEFT*9, truck.get_center()).set_color(OBJ_A)
        ))
        self.play(MoveAlongPath(truck, path),rate_func=linear)
        self.wait()

class PacketDetail(Scene):

    ether =  """
    00 08 E3 FF DF 09 AC C9 06 21
    A3 9C 08 00
    """
    ip = """
    45 00 00 43 00 01 00 00 40 06
    9A EE 0A 0B 0B 0B 68 12 24 40
    """
    transport = """
    00 14 00 50 00 00 00 00 00 00
    00 00 50 02 20 00 DD EB 00 00
    """
    app = """
    47 45 54 20 2F 69 6E 64 65 78
    2E 68 74 6D 6C 20 48 54 54 50
    2F 31 2E 30 20 0A 0A
    """

    def create_packet(self):
        # 设置车厢的尺寸
        carriage_height = 2.0
        carriage_width = 4.0
        
        # 设置车头的尺寸
        cab_height = 1.5
        cab_width = 1.25
        
        # 创建车厢的矩形
        carriage = Rectangle(height=carriage_height, width=carriage_width)
        carriage.set_fill(OBJ_B, opacity=0.3) # 设置填充颜色和不透明度
        
        # 创建车头的矩形
        cab = Rectangle(height=cab_height, width=cab_width)
        cab.set_fill(OBJ_C, opacity=0.3) # 设置填充颜色和不透明度
        
        #将车头放置在车厢旁边
        cab.next_to(carriage, RIGHT, buff=0)
        
        # 对整个货车进行组合
        truck = VGroup(carriage, cab).scale(0.5)
        
        # 将货车放置在屏幕中心
        truck.move_to(ORIGIN)
        return truck

    def create_stack(self, length=5,height=0.5,color=OBJ_A):
        stack = VGroup()
        for i in range(length):
            r_color = OBJ_A
            height = height
            rect = Rectangle(color=r_color, fill_opacity=0.2, width=3, height=height,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(stack, DOWN, buff=0)
            stack.add(rect)
        stack.move_to(ORIGIN)
        return stack

    def construct(self):
        
        # 将货车添加到场景中
        truck = self.create_packet()
        self.add(truck)

        path = Line(LEFT*9, RIGHT*9)
        packets = VMobject()
        self.add(path, packets)
        packets.add_updater(lambda x: x.become(
            Line(LEFT*9, truck.get_center()).set_color(OBJ_A)
        ))
        self.play(MoveAlongPath(truck, path),rate_func=linear)
        path_origin = Line(LEFT*9, ORIGIN)
        self.play(MoveAlongPath(truck, path_origin),rate_func=linear)

        self.remove(path, path_origin, packets)
        self.play(truck.animate.scale(3))
        
        lapp = Text(self.app, color=OBJ_C).scale(0.4).move_to(truck[0]).shift(UP)
        ltrans = Text(self.transport, color=OBJ_B).scale(0.4).next_to(lapp, DOWN, buff=0.1)
        lip = Text(self.ip, color=OBJ_A).scale(0.4).next_to(ltrans, DOWN, buff=0.1)
        lether = Text(self.ether, color=WORD_A).scale(0.4).next_to(lip, DOWN, buff=0.1)

        protocols = VGroup(lapp, ltrans, lip, lether)

        self.play(
            FadeIn(lether),
            FadeIn(lip),
            FadeIn(ltrans),
            FadeIn(lapp),
        )

        self.play(FadeOut(truck))

        self.play(protocols.animate.shift(LEFT*3))

        tcpip = self.create_stack(5, height=1)

        glevel = VGroup()
        levels = ["嘴层", "应用层", "运输层","网络层",  "物理链路层",]
        for i in range(len(levels)):
            color = WORD_A
            if not i:
                color=WORD_B
            glevel.add(Text(levels[i], color=color).scale(0.8).move_to(tcpip[i]))

        customize_proto = VGroup(glevel, tcpip)

        self.play(FadeIn(customize_proto))
        self.play(customize_proto.animate.shift(RIGHT*3))
        self.play(FadeOut(customize_proto[0]))

        ethersrc = lether[0:12]
        etherdst = lether[12:24]
        # ip v4?
        ethertype = lether[-4:]

        tethersrc  = Text("SRC: 00-08-E3-FF-DF-09",color=WORD_A).scale(0.2).move_to(tcpip[4]).shift(UP*0.3)
        tetherdst  = Text("DST: CA-C9-06-21-A3-9C",color=WORD_A).scale(0.2).next_to(tethersrc, DOWN, buff=0.1)
        tetherproto  = Text("IPV4",color=WORD_A).scale(0.2).next_to(tetherdst, DOWN, buff=0.1)

        self.play(Indicate(ethersrc))
        self.play(ethersrc.animate.become(tethersrc))
        self.play(Indicate(etherdst))
        self.play(etherdst.animate.become(tetherdst))
        self.play(Indicate(ethertype))
        self.play(ethertype.animate.become(tetherproto))

        ipsrc = lip[-16:-8]
        ipdst = lip[-8:]
        iptype = lip[-22:-20]
        tipsrc = Text("SRC: 10.11.11.11", color=OBJ_A).scale(0.2).move_to(tcpip[3]).shift(UP*0.3)
        tipdst = Text("DST: 104.18.36.64", color=OBJ_A).scale(0.2).next_to(tipsrc, DOWN, buff=0.1)
        tiptype = Text("PROTO: TCP ", color=OBJ_A).scale(0.2).next_to(tipdst, DOWN, buff=0.1)

        self.play(Indicate(ipsrc))
        self.play(ipsrc.animate.become(tipsrc))
        self.play(Indicate(ipdst))
        self.play(ipdst.animate.become(tipdst))
        # tcp or udp?
        self.play(Indicate(iptype))
        self.play(iptype.animate.become(tiptype))

        tcpsrcport = ltrans[0:4]
        tcpdstport = ltrans[4:8]
        ttcpsrcport = Text("SRC PORT: 20", color=OBJ_B).scale(0.2).move_to(tcpip[2]).shift(UP*0.2)
        ttcpdstport = Text("DST PORT: 80", color=OBJ_B).scale(0.2).next_to(ttcpsrcport, DOWN)
        self.play(Indicate(tcpsrcport))
        self.play(tcpsrcport.animate.become(ttcpsrcport))
        self.play(Indicate(tcpdstport))
        self.play(tcpdstport.animate.become(ttcpdstport))

        appmsg = Text("GET /index.html HTTP/1.0", color=OBJ_C).scale(0.2).move_to(tcpip[1])
        self.play(lapp.copy().animate.become(appmsg))

        timeout = Text("TIMEOUT: 60s", color=WORD_B).scale(0.4).move_to(tcpip[0])
        self.play(FadeIn(timeout))

        self.wait()
