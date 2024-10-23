Here's how you can set up the Ansible solution for the given requirements:

## 1. Ansible Inventory File
This file defines the three servers hosting the services (`httpd` on `host1`, `rabbitMQ` on `host2`, and `postgreSQL` on `host3`).
#### `inventory:`
```ini
[web]
host1 ansible_host=your_host1_ip ansible_user=your_user

[messaging]
host2 ansible_host=your_host2_ip ansible_user=your_user

[database]
host3 ansible_host=your_host3_ip ansible_user=your_user

[all:vars]
ansible_ssh_private_key_file=~/.ssh/id_rsa  # Adjust to your SSH key file

```
## 2. Ansible Playbook
Below is an Ansible playbook that handles three tasks (`verify_install`, `check-disk`, and `check-status`) based on the provided `action` variable.

#### `assignment.yml:`
```yml
---
- name: Verify and Monitor RHEL services
  hosts: all
  vars:
    email_address: "your_email@example.com"  # Replace with your alert email
  tasks:

    - name: Verify and install services
      when: action == "verify_install"
      block:
        - name: Verify httpd installation on host1
          when: inventory_hostname == "host1"
          yum:
            name: httpd
            state: present

        - name: Verify rabbitmq-server installation on host2
          when: inventory_hostname == "host2"
          yum:
            name: rabbitmq-server
            state: present

        - name: Verify postgresql installation on host3
          when: inventory_hostname == "host3"
          yum:
            name: postgresql-server
            state: present

    - name: Check disk usage and send alert if usage > 80%
      when: action == "check-disk"
      block:
        - name: Check disk usage
          shell: "df -h | awk '$5 > 80 {print $0}'"
          register: disk_usage
          ignore_errors: yes

        - name: Send alert email if high disk usage found
          mail:
            host: localhost
            port: 25
            to: "{{ email_address }}"
            subject: "Disk Usage Alert on {{ inventory_hostname }}"
            body: "{{ disk_usage.stdout }}"
          when: disk_usage.stdout != ""

    - name: Check application status
      when: action == "check-status"
      block:
        - name: Get the application status via REST API
          uri:
            url: "http://{{ hostvars['host1'].ansible_host }}:5000/healthcheck"
            method: GET
            return_content: yes
          register: healthcheck

        - name: Display application status
          debug:
            msg: "Application Status: {{ healthcheck.json.application_status }}"

        - name: Check individual service status
          block:
            - name: Check httpd status
              uri:
                url: "http://{{ hostvars['host1'].ansible_host }}:5000/healthcheck/httpd"
                method: GET
                return_content: yes
              register: httpd_status

            - name: Check rabbitmq status
              uri:
                url: "http://{{ hostvars['host1'].ansible_host }}:5000/healthcheck/rabbitmq-server"
                method: GET
                return_content: yes
              register: rabbitmq_status

            - name: Check postgresql status
              uri:
                url: "http://{{ hostvars['host1'].ansible_host }}:5000/healthcheck/postgresql"
                method: GET
                return_content: yes
              register: postgresql_status

          always:
            - name: Display services down
              debug:
                msg: >
                  Services Down: {{
                    (httpd_status.json.service_status != 'UP' | ternary('httpd', ''))
                    + (rabbitmq_status.json.service_status != 'UP' | ternary(' rabbitmq-server', ''))
                    + (postgresql_status.json.service_status != 'UP' | ternary(' postgresql', ''))
                  | trim }}

```
# Explanation
### 1. verify_install:

- Checks if the services are installed on their respective servers.
- Installs missing services using `yum`.
- Adjust the package name if necessary depending on your RHEL configuration.
### 2. check-disk:

- Executes a shell command to check if any mounted filesystem has disk usage greater than 80%.
- Sends an alert email if the threshold is exceeded using the `mail` module.
### 3.check-status:

- Uses the REST API (created in TEST1) to check the overall application status and individual services.
- Uses the `uri` module to interact with the API and report any services that are down.

# Command to Run the Playbook
To run the playbook for each action, use the following command:
```bash
ansible-playbook assignment.yml -i inventory -e action=verify_install
```
Replace `verify_install` with `check-disk` or `check-status` depending on the task you want to perform.

