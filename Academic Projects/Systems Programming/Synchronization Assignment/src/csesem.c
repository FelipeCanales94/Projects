#include <pthread.h>
#include <stdlib.h>

#include "csesem.h"

/* This definition of struct CSE_Semaphore is only available _inside_
 * your semaphore implementation.  This prevents calling code from
 * inadvertently invalidating the internal representation of your
 * semaphore.  See csesem.h for more information.
 *
 * You may place any data you require in this structure. */
struct CSE_Semaphore {
	pthread_mutex_t *mutex;
	pthread_cond_t *cond;
	int counter;
};

/* This function must both allocate space for the semaphore and perform
 * any initialization that is required for safe operation on the
 * semaphore.  Te user should be able to immediately call csesem_post()
 * or csesem_wait() after this routine returns. */
CSE_Semaphore csesem_create(int count) {
	CSE_Semaphore sem;
	if(count < 0 )
		return NULL;
    sem = calloc(1, sizeof(struct CSE_Semaphore));
    if(sem == NULL)
    	return NULL;
    sem->mutex = calloc(1,sizeof(pthread_mutex_t));
    if(sem->mutex == NULL)
    {
    	free(sem);
    	return NULL;
    }
    sem->cond = calloc(1,sizeof(pthread_cond_t));
    if(sem->cond == NULL)
    {
    	free(sem->mutex);
    	free(sem);
    	return NULL;
    }
    sem->counter = count;
    pthread_mutex_init(sem->mutex,0);
    pthread_cond_init(sem->cond,0);
    return sem;
}

void csesem_post(CSE_Semaphore sem) {
	if(sem == NULL)
		return;
	pthread_mutex_lock(sem->mutex);
	(sem->counter)++;
	pthread_mutex_unlock(sem->mutex);
	pthread_cond_signal(sem->cond);
}

void csesem_wait(CSE_Semaphore sem) {
	if(sem == NULL)
		return;
	pthread_mutex_lock(sem->mutex);
	while(sem->counter == 0)
		pthread_cond_wait(sem->cond, sem->mutex);
	(sem->counter)--;
	pthread_mutex_unlock(sem->mutex);
}

/* This function should destroy any resources allocated for this
 * semaphore; this includes mutexes or condition variables. */
void csesem_destroy(CSE_Semaphore sem) {
	if(sem == NULL)
		return;
	pthread_mutex_destroy(sem->mutex);
	pthread_cond_destroy(sem->cond);
}
