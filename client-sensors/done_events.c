#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <ctype.h>
#include <time.h>
//#include "glite/wmsutils/jobid/cjobid.h"
#include "glite/jobid/cjobid.h"
#ifdef BUILDING_LB_CLIENT
#include "consumer.h"
#else
#include "glite/lb/consumer.h"
#endif

static void usage(char *me) {
	fprintf(stderr,"usage: %s: YYYY-MM-DD:HH:MI:SS YYYY-MM-DD:HH:MI:SE\n"
			"\t times specify interval to query\n",me
		);
	exit(1);
}

int main(int argc,char **argv) {

        /* VARIABLES DECLARATION */ 
	edg_wll_Context	ctx;
	struct tm	tm;
	time_t	from,to;
	int	i, err = 0;

        /* VARIABLES INITIALIZATION */ 
	edg_wll_QueryRec	cond[3];	/* [2] is terminator */
	edg_wll_Event	*events = NULL;

	edg_wll_InitContext(&ctx);

	if (argc != 3) usage(argv[0]);
	memset(&tm,0,sizeof tm);
	if (sscanf(argv[1],"%d-%d-%d:%d:%d:%d",
		&tm.tm_year,
		&tm.tm_mon,
		&tm.tm_mday,
		&tm.tm_hour,
		&tm.tm_min,
                &tm.tm_sec)!= 6) usage(argv[0]);

	tm.tm_mon--;
	tm.tm_year -= 1900;
	from = timegm(&tm);

	memset(&tm,0,sizeof tm);
	if (sscanf(argv[2],"%d-%d-%d:%d:%d:%d",
		&tm.tm_year,
		&tm.tm_mon,
		&tm.tm_mday,
		&tm.tm_hour,
		&tm.tm_min,
                &tm.tm_sec) != 6) usage(argv[0]);

	tm.tm_mon--;
	tm.tm_year -= 1900;
	to = timegm(&tm);
	memset(cond,0,sizeof cond);

        /* QUERY CONDITIONS INITIALIZATION: ALL JOBS DONE WITHIN TIME INTERVAL */
	cond[0].attr = EDG_WLL_QUERY_ATTR_TIME;
	cond[0].op = EDG_WLL_QUERY_OP_WITHIN;
	cond[0].value.t.tv_sec = from;
	cond[0].value2.t.tv_sec = to;

	cond[1].attr = EDG_WLL_QUERY_ATTR_EVENT_TYPE;
	cond[1].value.i = EDG_WLL_EVENT_DONE;
	
	if (edg_wll_QueryEventsProxy(ctx,NULL,cond,&events)) {
		char	*et,*ed;
        	et = ed = NULL;

		edg_wll_Error(ctx,&et,&ed);
		fprintf(stderr,"edg_wll_QueryEventsProxy: %s, %s\n",
			et,ed ? ed : "");

		free(et); free(ed);
		err = 1;
		goto cleanup;
	}

        /* SELECTION OF DONE FAILED-OR-OK JOBS */
//   printf("SELECTION OF DONE JOBS\n");
//   printf("OWNER\tJOBID\tEXITCODE\tTIMESTAMP\tFAILUREREASON\n");     
	for (i=0; events[i].type; i++) {
		edg_wll_Event	*e = events+i;
                if(e->done.status_code == EDG_WLL_DONE_OK) {
                        char    *job = glite_jobid_unparse(e->any.jobId);

                        printf("%s\t%s\t%s",
                                e->any.user,
                                job,
                                ctime(&e->done.timestamp.tv_sec)
                                //asctime(gmtime(&e->done.timestamp.tv_sec))
                                );
                        free(job);
                }

/*		if (e->done.status_code == EDG_WLL_DONE_FAILED) {
			char	*job = glite_jobid_unparse(e->any.jobId);                        
                        printf("%s\t%s\t%d\t%s\t%s\n",
                                e->any.user,
                                job,
                                e->done.status_code,
                                ctime(&e->done.timestamp.tv_sec),
                                e->done.reason
                                );
			free(job);
		} else if(e->done.status_code == EDG_WLL_DONE_OK) {
			char	*job = glite_jobid_unparse(e->any.jobId);

                        printf("%s\t%s\t%d\t%s\tNULL\n",
                                e->any.user,
                                job,
                                e->done.status_code,
                                ctime(&e->done.timestamp.tv_sec)                               
                                );
			free(job);}*/
	}
				
cleanup:
	if (events) {
		for (i=0; events[i].type; i++) edg_wll_FreeEvent(events+i);
		free(events); events = NULL;
	}

	edg_wll_FreeContext(ctx);

	return err;
}
