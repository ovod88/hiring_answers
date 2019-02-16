import sys
import socket
import json
import ast

#TODO add check of entered IP address (if correct subnet or correct IP)
#TODO add parallel threads to TCP/UDP scanner for chosen library which can use only one type at once
#TODO Rebuild script to OOP style with scanner class for future scale
#TODO Add script description so user knows what parameters to enter
#Also make port range also as a parameter
#TODO Think on how to remove a triple loop
ips_to_scan = []

provided_ip_address = sys.argv[1]

ip_address = provided_ip_address.split('/')[0]
try:
	ip_mask = provided_ip_address.split('/')[1]
except:
	ip_mask = None

if ip_mask is None:
	ips_to_scan.append(ip_address)
else:
	net_address_bytes = ip_address.split('.')
	net_address_bytes_binary = []

	num_of_ones = int(ip_mask)
	num_of_zeros = 32 - num_of_ones
        
	for octet in net_address_bytes:
		binary_byte = bin(int(octet)).lstrip('0b')
		net_address_bytes_binary.append(binary_byte.zfill(8))
            


	binary_net = "".join(net_address_bytes_binary)
	broadcast_address_binary = binary_net[:(num_of_ones)] + "1" * num_of_zeros

	bst_net_bytes = []
	    
	for bit in range(0, 32, 8):
		bst_net_byte = broadcast_address_binary[bit: bit + 8]
		bst_net_bytes.append(bst_net_byte)

	bst_net_address = []

	for each_byte in bst_net_bytes:
		bst_net_address.append(str(int(each_byte, 2)))

	broadcast_address = ".".join(bst_net_address)

	# print('B', broadcast_address)
	generated_ip = []

	for indexB, oct_B in enumerate(bst_net_address):
		for indexN, oct_N in enumerate(net_address_bytes):
			if indexB == indexN:
				if oct_B == oct_N:
					generated_ip.append(oct_B)
				else:
					first_ip_part = generated_ip

					for ip in range(int(oct_N) + 1, int(oct_B)):
						ips_to_scan.append('.'.join(first_ip_part) + '.' + str(ip))

def idIdenticalLists(list1, list2):
	return not any(a != b for a, b in zip(list1, list2)) and len(list1) == len(list2)

saved_results_json = {}

try:
	with open("result.txt", 'r') as file:
		saved_results_json = json.load(file)
except Exception as e:
	pass
finally:
	for host in ips_to_scan:
		host_result = {}
		prev_result = {}

		host_result[host] = []

		try:
			prev_result[host] = saved_results_json[host]
		except KeyError as e:
			prev_result[host] = []

		for port in range(1,1024):
			sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			result_tcp = sock_tcp.connect_ex((host, port)) 

			if result_tcp == 0:
				host_result[host].append(dict(port=port, protocol='tcp'))
			sock_tcp.close()

		if idIdenticalLists(host_result[host], prev_result[host]):
			print("*Target - {host}: No new records found in the last scan.*".format(host=host))	
		else:
			print("*Target - {host}: Full scan results:*".format(host=host))

			for port_res in host_result[host]:
				print("Host: {host} Ports: {port}/open/tcp////".format(host=host, \
																port=port_res['port']))
			saved_results_json[host] = host_result[host]

			# print(saved_results_json)

			with open("result.txt", 'w') as file:
				json.dump(saved_results_json, file, indent=4)