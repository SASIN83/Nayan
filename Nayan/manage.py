#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import ssl

if not hasattr(ssl, 'wrap_socket'):
    def dummy_wrap_socket(sock, keyfile=None, certfile=None,
                          server_side=False, cert_reqs=ssl.CERT_NONE,
                          ssl_version=ssl.PROTOCOL_TLS, ca_certs=None,
                          do_handshake_on_connect=True,
                          suppress_ragged_eofs=True,
                          ciphers=None):
        
        context = ssl.SSLContext(ssl_version)
        if certfile:
            context.load_cert_chain(certfile, keyfile)
        if ca_certs:
             context.load_verify_locations(ca_certs)
        if cert_reqs:
            context.verify_mode = cert_reqs
            
        return context.wrap_socket(
            sock, 
            server_side=server_side, 
            do_handshake_on_connect=do_handshake_on_connect, 
            suppress_ragged_eofs=suppress_ragged_eofs
        )
    
    ssl.wrap_socket = dummy_wrap_socket

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nayan.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
