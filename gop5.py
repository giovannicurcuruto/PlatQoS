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
 temp = [int(i,16) for i in temp]
 temp = "".join(map(chr,temp))
 return temp
 
def main(argv):
#função para ler do arquivo
	
   y = open('./mac_src', 'r')
   y_1 = y.readline()     
   src = y_1.replace('\n','')
   y.close()

   z = open('./mac_dest', 'r')
   z_1 = z.readline()     
   dest = z_1.replace('\n','')
   z.close()

   ethernet_data_str = "Em um alfabeto de mudos, o fofoqueiro é depressivo"
	##############
	
	#############
	# Prioridades:
	# 0 - 00:01 
	# 1 - 20:01 
	# 2 - 40:01
	# 3 - 60:01
	# 4 - 80:01
	# 5 - A0:01 X
	# 6 - C0:01
	# 7 - E0:01


   prio = "A0:01"
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


   x = open('./interface', 'r')
   x_1 = x.readline()     
   interface = x_1.replace('\n','')
 
   x.close()
   protocol = 0 
 
   print 'MAC FONTE', src
   print 'MAC DESTINO', dest
   print 'INTERFACE', interface
 
  
   s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW) 
   s.bind((interface,protocol))    
 
   ethernet_hdr_str = build_ethernet_hdr(dest, src, proto)
 

   s.send(ethernet_hdr_str + ethernet_data_str)    

 
if __name__ == "__main__":
   main(sys.argv[1:])
