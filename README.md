[![Build Status](https://travis-ci.com/Courouge/ansible-beautify.svg?branch=master)](https://travis-ci.com/Courouge/ansible-beautify)

### Ansible beautify tasks [One-liner ansible syntax to multiligne full yaml]

## Transform this ↓
```
- name: Insert trololo
  lineinfile: dest=/etc/trololo state=present regexp="{{ trololo }}" insertafter="trololo" line="trololo"
  notify: restart trololo
```
## To that ↓
```
- name: Insert trololo
  lineinfile:
    dest: /etc/trololo
    regexp: {{ trololo }}
    insertafter: trololo
    line: trololo
    state: present
  notify: restart trololo
```

Support all module !
If you have your own library, no problem add it on the modules.txt file :)

### Running
sudo docker-compose up -d --force-recreate --build && sudo docker-compose up

check ==> http://localhost:3000/
