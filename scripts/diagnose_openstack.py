#!/usr/bin/env python3
"""
OpenStack Diagnose
"""
import os
from dotenv import load_dotenv
from openstack import connection
import json

def diagnose_openstack_access():
    load_dotenv()
    
    print("=== OpenStack API Test ===")
    print(f"Username: {os.environ.get('OS_USERNAME')}")
    print(f"Project: {os.environ.get('OS_PROJECT_NAME')}")
    print(f"Auth URL: {os.environ.get('OS_AUTH_URL')}")
    print()
    
    try:
        conn = connection.Connection(
            auth_url=os.environ.get('OS_AUTH_URL'),
            project_name=os.environ.get('OS_PROJECT_NAME'),
            username=os.environ.get('OS_USERNAME'),
            password=os.environ.get('OS_PASSWORD'),
            user_domain_name=os.environ.get('OS_USER_DOMAIN_NAME', 'default'),
            project_domain_name=os.environ.get('OS_PROJECT_DOMAIN_NAME', 'default'),
            verify=False,
        )
        
        print("✅ OpenStack")
        
        # 1. Connection
        try:
            token = conn.identity.get_token()
            print(f"✅ Identity Token: ", token)
            
            # Connect with user and project
            user_id = conn.current_user_id
            project_id = conn.current_project_id
            
            # List all roles
            for role in conn.identity.roles():
                print("Role:",role.name)
            
            #for assignment in roles:
            #    role_id = assignment.role['id']
            #    role = conn.identity.get_role(role_id)
            #    print(f"  - {role.name}")
                
        except Exception as e:
            print(f"❌ Error connecting: {e}")
        
        print()
        
         # 2. Hypervisor
        print("--- Hypervisor  ---")
        try:
            hypervisors = list(conn.compute.hypervisors(details=True))
            print(f"✅ Hypervisor : {len(hypervisors)}개")
            
            for hyp in hypervisors:
                print(f"Hypervisor ID: {hyp.id}")
                print(f"  Hostname: {getattr(hyp, 'hypervisor_hostname', 'N/A')}")
                print(f"  Status: {getattr(hyp, 'status', 'N/A')}/{getattr(hyp, 'state', 'N/A')}")
                print(f"  vCPUs: {getattr(hyp, 'vcpus_used', 'N/A')}/{getattr(hyp, 'vcpus', 'N/A')}")
                print(f"  memory: {getattr(hyp, 'memory_mb_used', 'N/A')}/{getattr(hyp, 'memory_mb', 'N/A')} MB")
                print(f"  VM running: {getattr(hyp, 'running_vms', 'N/A')}")
                print(f"  hyperv type: {getattr(hyp, 'hypervisor_type', 'N/A')}")
                print()
                
        except Exception as e:
            print(f"❌ Hypervisor : {e}")
        
        print()
        
        # 3. servers
        print("--- Servers ---")
        try:
            servers = list(conn.compute.servers(details=True))
            print(f"✅ Servers: {len(servers)}")
            
            total_vcpus_used = 0
            total_memory_used = 0
            
            #for server in servers:
            #    flavor = conn.compute.get_flavor(server.flavor['id'])
            #    total_vcpus_used += flavor.vcpus
            #    total_memory_used += flavor.ram
                
            #    print(f"Name: {server.name}")
            #    print(f"  Status: {server.status}")
            #    print(f"  Flavor vCPUs: {flavor.vcpus}")
            #    print(f"  Flavor RAM: {flavor.ram} MB")
            #    print(f"  Attr: {getattr(server, 'OS-EXT-SRV-ATTR:host', 'N/A')}")
            
            #print(f"\n📊 Utilization:")
            #print(f"  vCPUs : {total_vcpus_used}")
            #print(f"  memory: {total_memory_used} MB")
                
        except Exception as e:
            print(f"❌ Error servers: {e}")
        
        print()
        
         # 4. Quota
        print("--- Quota ---")
        try:
            project_id = conn.current_project_id
            quotas = conn.compute.get_quota_set(project_id)
            
            print(f"✅ Quota project:")
            print(f"  instances: {getattr(quotas, 'instances', 'N/A')}")
            print(f"  Cores: {getattr(quotas, 'cores', 'N/A')}")
            print(f"  RAM: {getattr(quotas, 'ram', 'N/A')} MB")
            
        except Exception as e:
            print(f"❌ Quota error: {e}")
        
        print()
        
        # 5. Compute usage
        print("--- Compute usage ---")
        try:
            project_id = conn.current_project_id
            usage = conn.compute.get_usage(project_id)
            
            print(f"✅ Compute usage:")
            print(f"  instances: {getattr(usage, 'total_instance_usage', 'N/A')}")
            print(f"  vCPU: {getattr(usage, 'total_vcpus_usage', 'N/A')}")
            print(f"  memory: {getattr(usage, 'total_memory_mb_usage', 'N/A')}")
            
        except Exception as e:
            print(f"❌ compute usage error: {e}")
            
            
            
    except Exception as e:
        print(f"❌ OpenStack connection error: {e}")

if __name__ == "__main__":
    diagnose_openstack_access()
