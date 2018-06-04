#Based on: https://gist.github.com/cslarsen/11339448
# -*- coding: utf-8 -*-  
import socket 
import re, uuid
import sys, getopt 
 
def build_ethernet_hdr(dest, src, proto):
 dest = "0x" + dest.replace(":", ",0x").upper()
 src = "0x" + src.replace(":", ",0x").upper()
 proto = "0x" + proto.replace(":",",0x").upper()
 temp = dest + "," + src + "," + proto
 temp = temp.split(",")
#	 print temp
 temp = [int(i,16) for i in temp]
 temp = "".join(map(chr,temp))
 return temp
 
def main(argv):
   src = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
   dest = ''
   ethernet_data_str = "vish"
	##############
	
	#############
	# Prioridades:
	# 0 - 00:01
	# 1 - 20:01
	# 2 - 40:01
	# 3 - 60:01
	# 4 - 80:01
	# 5 - A0:01
	# 6 - C0:01
	# 7 - E0:01


   prio = "C0:00"
   proto = "81:00" + ":" + prio
   try:
      opts, args = getopt.getopt(argv,"hs:d:i:",["src=","dst=", "info="])
   except getopt.GetoptError:
      print 'sendraw.py -s <mac_src> -d <mac_dst> -c <data>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'sendraw.py -s <mac_src> -d <mac_dst> -i <data>'
         sys.exit()
      elif opt in ("-s", "--src"):
           src = arg
      elif opt in ("-d", "--dst"):
           dest = arg
      elif opt in ("-i", "--info"):
           ethernet_data_str = arg
      elif opt in ("-p", "--proto"):
           proto = arg

   interface = "lo" # Set this to your Ethernet interface (e.g. eth0, eth1, ...) 
   protocol = 0 # 0 = ICMP, 6 = TCP, 17 = UDP, ...
 
   print 'MAC FONTE', src
   print 'MAC DESTINO', dest
   print 'INTERFACE', interface
 
  
   # Create and bind a raw socket with address family PACKET 
   s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW) 
   s.bind((interface,protocol)) 
  
   # Create an Ethernet frame header 
   # - Destination MAC: 6 Bytes 
   # - Source MAC: 6 Bytes 
   # - Type: 2 Bytes (IP = 0x0800) 
   # Change the MAC addresses to match the your computer and the destination 
   # ethernet_hdr = [0x9a, 0x5f, 0xb4, 0x08, 0xa7, 0xd2, # 00:23:69:3A:F4:7D 
   #            0x96, 0x1d, 0xee, 0xb1, 0xb4, 0x4e, # 90:2b:34:60:dc:2f 
   #            0x00, 0x00] 
 
   ethernet_hdr_str = build_ethernet_hdr(dest, src, proto)
 
   # Frame structure: 
   # etherent_hdr | ethernet_data 
   #    14 B   |    5 B 
  
   # ethernet_data_str = sys.argv[2] 
  
   # Convert byte sequences to strings for sending 
   #ethernet_hdr_str = "".join(map(chr, ethernet_hdr)) 
#   print ethernet_hdr_str
  
   # Send the frame
#   s.send(ethernet_hdr_str + ethernet_data_str)
   loop	= 0
   x = 1
   while (loop < 10000):
        x = x + 1
	s.send(ethernet_hdr_str + ethernet_data_str)    
	print x
        loop = loop + 1
   
   

 
if __name__ == "__main__":
   main(sys.argv[1:])
