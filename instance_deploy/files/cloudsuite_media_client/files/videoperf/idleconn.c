/*
    httperf -- a tool for measuring web server performance
    Copyright (C) 2000  Hewlett-Packard Company
    Contributed by David Mosberger-Tang <davidm@hpl.hp.com>

    This file is part of httperf, a web server performance measurment
    tool.

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
    02111-1307 USA
*/

#include <errno.h>
#include <netdb.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <netinet/in.h>
#include <arpa/inet.h>

#include <sys/time.h>
#include <sys/types.h>
#include <sys/resource.h>
#include <sys/socket.h>

const char *prog_name;
unsigned long num_conn, num_closed;
struct timeval start_time;

void
sigint_handler (int signal)
{
  struct timeval stop_time;
  double delta_t;

  gettimeofday (&stop_time, NULL);

  delta_t = ((stop_time.tv_sec - start_time.tv_sec)
	     + 1e-6*(stop_time.tv_usec - start_time.tv_usec));

  printf ("%s: total # conn. created = %lu, close() rate = %g conn/sec\n",
	  prog_name, num_conn, num_closed / delta_t);
  exit (0);
}

int
main (int argc, char **argv)
{
  int desired, current = 0, port, sd, max_sd = 0, n, i;
  struct sockaddr_in sin, server_addr;
  fd_set readable, rdfds;
  struct rlimit rlimit;
  struct hostent *he;
  char *server;

  signal (SIGINT, sigint_handler);

  prog_name = strrchr (argv[0], '/');
  if (prog_name)
    ++prog_name;
  else
    prog_name = argv[0];

  memset (&rdfds, 0, sizeof (rdfds));

  if (argc != 4)
    {
      fprintf (stderr, "Usage: %s server port numidle\n", prog_name);
      exit (-1);
    }

  server = argv[1];
  port = atoi (argv[2]);
  desired = atoi (argv[3]);

  /* boost open file limit to the max: */
  if (getrlimit (RLIMIT_NOFILE, &rlimit) < 0)
    {
      fprintf (stderr, "%s: failed to get number of open file limit: %s",
	       prog_name, strerror (errno));
      exit (1);
    }

  if (rlimit.rlim_max > FD_SETSIZE)
    {
      fprintf (stderr, "%s: warning: open file limit = %ld > FD_SETSIZE\n"
               "  limiting max. # of open files to FD_SETSIZE = %ld\n",
               prog_name, (long int) rlimit.rlim_max, (long int) FD_SETSIZE);

      rlimit.rlim_max = FD_SETSIZE;
    }

  rlimit.rlim_cur = rlimit.rlim_max;
  if (setrlimit (RLIMIT_NOFILE, &rlimit) < 0)
    {
      fprintf (stderr, "%s: failed to increase number of open file limit: %s",
	       prog_name, strerror (errno));
      exit (1);
    }

  printf ("%s: creating and maintaining %d idle connections\n",
	  prog_name, desired);

  memset (&server_addr, 0, sizeof (server_addr));
  server_addr.sin_family = AF_INET;
  server_addr.sin_port = htons (port);

  he = gethostbyname (server);
  if (he)
    {
      if (he->h_addrtype != AF_INET || he->h_length != sizeof (sin.sin_addr))
	{
	  perror (server);
	  exit (-1);
	}
      memcpy (&server_addr.sin_addr, he->h_addr_list[0],
	      sizeof (server_addr.sin_addr));
    }
  else
    if (!inet_aton (server, &server_addr.sin_addr))
      {
	fprintf (stderr, "%s: invalid server address %s\n", prog_name, server);
	exit (-1);
      }

  gettimeofday (&start_time, NULL);

  while (1)
    {
      while (current < desired)
	{
	  /* create more idle connections */
	  sd = socket (AF_INET, SOCK_STREAM, 0);
	  if (sd < 0)
	    {
	      perror ("socket");
	      exit (-1);
	    }

	  sin = server_addr;
	  if (connect (sd, (struct sockaddr *) &sin, sizeof (sin)) < 0)
	    {
	      printf("connect: %s\n", strerror (errno));
	      switch (errno)
		{
		case ECONNREFUSED:
		  /* wait for server to start up... */
		  usleep (1000000);
		case ETIMEDOUT:
		  close (sd);
		  continue;

		default:
		  perror ("connect");
		  exit (-1);
		}
	    }

	  if (sd > max_sd)
	    max_sd = sd;

#if DEBUG > 1
	  printf ("created %d\n", sd);
#endif
	  ++num_conn;
	  ++current;
	  FD_SET(sd, &rdfds);
	}

      readable = rdfds;
      n = select (max_sd + 1, &readable, NULL, NULL, NULL);
      for (i = 0; i <= max_sd; ++i)
	{
	  if (FD_ISSET (i, &readable))
	    {
#if DEBUG > 1
	      printf ("closed %d\n", i);
#endif
	      close (i);
	      --current;
	      --n;
	      ++num_closed;
	      FD_CLR(i, &rdfds);
	    }
	  if (n <= 0)
	    break;
	}
    }
}
