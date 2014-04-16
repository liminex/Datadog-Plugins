#Ok = 0
#Some error = 1
#!/usr/bin/python 2.6

import os
import sys
import subprocess

from checks import AgentCheck

class define(AgentCheck):
  def check(self,instance):
    default_timeout = self.init_config.get('default_timeout', 5)

    replicator_running = subprocess.Popen("/home/tungsten/installs/cookbook/tungsten/tungsten-replicator/bin/replicator status | grep PID | wc -l", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE )

    metric_count = 0

    p_stdout = replicator_running.stdout.read().strip()

    metric = p_stdout

    self.gauge('tungsten_status', metric, tags=['check_tungsten_status'])

if __name__ == '__main__':
  check, instances = define.from_yaml('/etc/dd-agent/conf.d/tungsten.yaml')
  for instance in instances:
    print "\nRunning the check"
    check.check(instance)
    print 'Metrics: %s' % (check.get_metrics())

 
