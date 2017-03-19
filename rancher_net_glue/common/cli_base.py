from __future__ import absolute_import, print_function


def validate_rancher_args(args):
    if not args.rancher_url:
        print ("error: Missing Rancher URL parameter")
        return False

    if not args.access_key:
        print ("error: Missing Rancher access key parameter")
        return False

    if not args.secret_key:
        print ("error: Missing Rancher secret key parameter")
        return False

    if not args.project_id:
        print ("error: Missing Rancher project id parameter")
        return False

    return True

def add_ranche_args(named_args):
    named_args.add_argument('--rancher-url',
                            help='Rancher api url (defaults to http://localhost:8080)')
    named_args.add_argument('--access-key', help='The Rancher access key')
    named_args.add_argument('--secret-key', help='The Rancher secret key')
    named_args.add_argument('--project-id', help="Rancher's project id")
