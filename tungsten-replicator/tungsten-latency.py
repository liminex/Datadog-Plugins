#!/usr/bin/python2.6

import os
import sys
import subprocess

from checks import AgentCheck

class details(AgentCheck):

  def check(self,instance):
    default_timeout = self.init_config.get('default_timeout', 5)
    replicator_latency = subprocess.Popen("/home/tungsten/installs/cookbook/tungsten/tungsten-replicator/bin/trepctl services | grep -E 'appliedLatency'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE )

    metric_count = 0
    res = replicator_latency.stdout.read()
    for ret in res.split('\n'):
      response = ret.split(': ')
      if len(response) == 2:
        metric, value = response
        try:
            value = float(value)
        except ValueError:
            continue
        self.gauge('tungsten_latency', value, tags=['check_tungsten_latency'])

if __name__ == '__main__':
  check, instances = details.from_yaml('/etc/dd-agent/conf.d/tungsten-latency.yaml')
  for instance in instances:
    print "\nRunning the check"
    check.check(instance)
    print 'Metrics: %s' % (check.get_metrics())



