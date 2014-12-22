#!/usr/bin/python2.6
import sys
import os
import subprocess

from checks import AgentCheck

class details(AgentCheck):

  GAUGES = {
    'start time':'php-fpm.start time',
    'start since':'php-fpm.start since',
    'accepted conn': 'php-fpm.connections',
    'listen queue': 'php-fpm.listen queue',
    'max listen queue': 'php-fpm.max listen queue',
    'active processes': 'php-fpm.active processes',
    'total processes': 'php-fpm.total processes',
    'max active processes': 'php-fpm.max active processes',
    'max children reached': 'php-fpm.max children reached',
  }

  def check(self, instance):
    default_timeout = instance.get('default_timeout', 5)
    fpm_status_uri = instance.get('fpm_status_uri', '/status')
    fpm_request_method = instance.get('fpm_request_method', 'GET')
    fpm_hostname = instance.get('fpm_hostname', '127.0.0.1')
    fpm_port = instance.get('fpm_port', 9000)
    os.environ["SCRIPT_NAME"] = os.environ["SCRIPT_FILENAME"] = fpm_status_uri
    os.environ["REQUEST_METHOD"] = fpm_request_method
    host_and_port = "%s:%d" % (fpm_hostname, fpm_port)
    req = subprocess.Popen(["cgi-fcgi", "-bind", "-connect", host_and_port], stdout=subprocess.PIPE).communicate()[0]
    metric_count = 0
    line = req
    for queue in line.split('\n'):
      values = queue.split(': ')
      if len(values) == 2:
        metric, value = values
        try:
            value = float(value)
        except ValueError:
            continue
      if metric in self.GAUGES:
        metric_count +=1
        check_fpm = self.GAUGES[metric]
        self.gauge(check_fpm, value, tags=['check_php-fpm'])

if __name__ == '__main__':
  check, instances = details.from_yaml('/etc/dd-agent/conf.d/php-fpm.yaml')
  for instance in instances:
    print "\nRunning the check"
    check.check(instances)
    print 'Metrics: %s' % (check.get_metrics())

