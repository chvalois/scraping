# stop_instance.py
import googleapiclient.discovery

def stop_instance(request):
    project = 'scraping-428507'
    zone = 'europe-west9-a'
    instance = 'scraping-gcp-e2'

    compute = googleapiclient.discovery.build('compute', 'v1')
    compute.instances().stop(project=project, zone=zone, instance=instance).execute()

    return 'Instance stopped'