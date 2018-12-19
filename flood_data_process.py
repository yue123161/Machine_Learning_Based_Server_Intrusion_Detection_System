#READ ME
#HTTP FEED : duration,flag,src_bytes,dst_bytes,urgent,wrong_fragment
#ICMP FEDD : duration,src_bytes,dst_bytes,count,srv_count
#UDP_TCP FEED : duration,flag,src_bytes,dst_bytes,count,srv_count

# KeyValue = Index
# duaration = 0
# protocol = 1
# service = 2
# flag = 3
# src_byte = 4
# dst_byte = 5
# land = 6
# wrong_frag = 7
# urgent = 8
# hot = 9
#in extractor
# count = 10
# srv_count = 11

#in data set
# count = 22
# srv_count = 23
import csv
class DataProcess:
    #TODO there is something wrong with number of flags we're mapping and number of flags that are in db do some more reasearch and solve the problem
    flag_map = {'S0':0,'S1':1,'S2':2,'S3':3,'SH':4,'SF':5,'OTH':6,'REJ':7,'RSTO':8,'RSTR':9,'RSTOS0':10,'RroSTC':11}
    class_map = {'normal':0,'anomaly':1}
    icmp_class_map = {'normal': 0, 'ipsweep': 1, 'nmap': 2, 'pod': 3, 'smurf': 4}
    df = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent',
           'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
           'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
           'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
           'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
           'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
           'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
           'dst_host_srv_rerror_rate', 'class']
    def prepareInstance(self,instance):
        # sample instance "0;tcp;private;S0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;123;6;1.00;1.00;0.00;0.00;0.05;0.07;0.00;255;26;0.10;0.05;0.00;0.00;1.00;1.00;0.00;0.00"
        #instance = "0;tcp;private;S0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;123;6;1.00;1.00;0.00;0.00;0.05;0.07;0.00;255;26;0.10;0.05;0.00;0.00;1.00;1.00;0.00;0.00"

        #Todo Writing Data Directly to File from here with class '0' seperate wirte file functionality later
        sr = instance.split(";")
        #print(sr)
        #TODO : Exception handling needed here
        if(sr[1].startswith("icmp")):
            csv_file = open('data/ICMP.csv', 'a+')
            writer = csv.DictWriter(csv_file, fieldnames=self.df)
            # ICMP FEED : duration,src_bytes,dst_bytes,count,srv_count
            df = {"duration":sr[0],"src_bytes":sr[4],"dst_bytes":sr[5],"count":sr[9],"srv_count":sr[10]}
            df_temp = df.copy()
            df_temp.update({'class':'normal'})
            writer.writerow(df_temp)
            protocol = 1
        else:
            if(sr[2].startswith("http")):
                csv_file = open('data/HTTP.csv', 'a+')
                writer = csv.DictWriter(csv_file, fieldnames=self.df)
                # HTTP FEED : duration,flag,src_bytes,dst_bytes,urgent,wrong_fragment
                df = {"duration": sr[0],"flag":sr[3] ,"src_bytes": sr[4], "dst_bytes": sr[5],"urgent": sr[8],"wrong_fragment": sr[7]}
                df_temp = df.copy()
                df_temp.update({'class': 'normal'})
                writer.writerow(df_temp)
                protocol=2
                df["flag"] = self.flag_map[df["flag"]]
            elif(sr[1].startswith("udp")):
                csv_file = open('data/UDP.csv', 'a+')
                writer = csv.DictWriter(csv_file, fieldnames=self.df)
                # UDP FEED :duration,src_bytes,dst_bytes,count,srv_count,diff_srv_rate,dst_host_count,dst_host_same_src_port_rate
                df = {"duration": sr[0],"src_bytes": sr[4], "dst_bytes": sr[5],"count":sr[9],"srv_count":sr[10],"diff_srv_rate":sr[16],"dst_host_count":sr[18],"dst_host_same_src_port_rate":sr[22]}
                df_temp = df.copy()
                df_temp.update({'class': 'normal'})
                writer.writerow(df_temp)
                protocol = 3
            else:
                csv_file = open('data/TCP.csv', 'a+')
                writer = csv.DictWriter(csv_file, fieldnames=self.df)
                # TCP FEED : duration,flag,src_bytes,dst_bytes,count,srv_count
                df = {"duration": sr[0], "flag": sr[3], "src_bytes": sr[4], "dst_bytes": sr[5],"count":sr[9],"srv_count":sr[10]}
                df_temp = df.copy()
                df_temp.update({'class': 'normal'})
                writer.writerow(df_temp)
                df["flag"]= self.flag_map[df["flag"]]
                protocol=4
        list = []
        for k, v in df.items():
            list.append(v)
        print("Protocol : "+str(protocol)+" Instance : "+str(list))
        return protocol,list
