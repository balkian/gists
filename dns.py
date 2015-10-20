# -*- coding: utf-8 -*-

from __future__ import print_function

try:
    from subprocess import getoutput
except ImportError:
    from commands import getoutput

from dnslib import RR,QTYPE,RCODE,A,parse_time
from dnslib.label import DNSLabel
from dnslib.server import DNSServer,DNSHandler,BaseResolver,DNSLogger
from docker import Client, errors

class DockerResolver(BaseResolver):
    """

    """
    def __init__(self, docker='unix://var/run/docker.sock',
                 origin='docker', ttl='60s'):
        self.client = Client(base_url=docker)
        self.origin = DNSLabel(origin)
        self.ttl = parse_time(ttl)

    def resolve(self,request,handler):
        reply = request.reply()
        qname = request.q.qname
        print("Queried: %s" % qname)
        print("Label: %s" % self.origin)
        found = False
        if not qname.matchSuffix(self.origin):
            print("Not the %s domain" % self.origin)
            return reply
        cname = "/" + str(qname.stripSuffix(self.origin))[:-1].replace("/", "_")
        try:
            for c in self.client.containers():
                if cname in c["Names"]:
                    container = self.client.inspect_container(c["Id"])
                    ns = container.get("NetworkSettings", {})
                    if ns:
                        address = ns.get("IPAddress", None)
                        print("Found %s [%s]" % (cname, address))
                        if address:
                            reply.add_answer(RR(qname,QTYPE.A,ttl=self.ttl,
                                                rdata=A(address)))
                    else:
                        print("Found %s - NO IP" % cname)
                    found = True
                    break
            if not found:
                print("Container not found: %s" % cname)
        except Exception as ex:
            print("Error occurred querying [%s]: %s" % (cname, ex))
        return reply

if __name__ == '__main__':

    import argparse,sys,time

    p = argparse.ArgumentParser(description="Docker DNS Resolver")
    p.add_argument("--docker","-d",default="unix://var/run/docker.sock",
                   metavar="<url>",
                   help="Docker Socket/URL (default: unix://var/run/docker.sock)")
    p.add_argument("--origin","-o",default="docker",
                    metavar="<origin>",
                    help="Origin domain label (default: .)")
    p.add_argument("--ttl","-t",default="60s",
                    metavar="<ttl>",
                    help="Response TTL (default: 60s)")
    p.add_argument("--port","-p",type=int,default=53,
                    metavar="<port>",
                   help="Server port (default:53)")
    p.add_argument("--address","-a",default="",
                   metavar="<address>",
                   help="Listen address (default:all)")
    p.add_argument("--udplen","-u",type=int,default=0,
                   metavar="<udplen>",
                   help="Max UDP packet length (default:0)")
    p.add_argument("--tcp",action='store_true',default=False,
                   help="TCP server (default: UDP only)")
    p.add_argument("--log",default="request,reply,truncated,error",
                   help="Log hooks to enable (default: +request,+reply,+truncated,+error,-recv,-send,-data)")
    p.add_argument("--log-prefix",action='store_true',default=False,
                   help="Log prefix (timestamp/handler/resolver) (default: False)")
    args = p.parse_args()

    resolver = DockerResolver(docker=args.docker, origin=args.origin, ttl=args.ttl)
    logger = DNSLogger(args.log,args.log_prefix)

    print("Starting Docker Resolver for %s (%s:%d) [%s]" % (
                        args.docker,
                        args.address or "*",
                        args.port,
                        "UDP/TCP" if args.tcp else "UDP"))

    if args.udplen:
        DNSHandler.udplen = args.udplen

    udp_server = DNSServer(resolver,
                           port=args.port,
                           address=args.address,
                           logger=logger)
    udp_server.start_thread()

    if args.tcp:
        tcp_server = DNSServer(resolver,
                               port=args.port,
                               address=args.address,
                               tcp=True,
                               logger=logger)
        tcp_server.start_thread()

    while udp_server.isAlive():
        time.sleep(1)
