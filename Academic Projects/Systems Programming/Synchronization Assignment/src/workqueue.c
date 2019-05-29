#include <pthread.h>
#include <stdlib.h>

#include "csesem.h"
#include "workqueue.h"

struct WorkItem {
    WQ_Function func;
    void *data;
};

/* You will need to modify this structure for your implementation.  You
 * will almost certainly need to use _at least_ the fields specified in
 * the given code.  It is very likely that you will need additional fields.
 *
 * You can modify anything in this structure, the tests will not assume
 * anything about its contents. */
struct WorkQueue {
    /* The number of slots in this work queue */
    int slots;

    /* A lock to protect the contents of this object */
    pthread_mutex_t lock;

    /* An array of available work items
     *
     * See the producer-consumer problem and implementation in Section
     * 12.5 of the text for information about these items and the items
     * associated with results.*/
    struct WorkItem *work;

    /* Front and rear indices for the work queue items */
    int work_front;
    int work_rear;

    /* Semaphores controlling the work queue */
    CSE_Semaphore work_slots;
    CSE_Semaphore work_items;

    /* An array of computed result objects */
    void **results;

    /* Front and rear indices for the results queue items */
    int results_front;
    int results_rear;

    /* Semaphores controlling the results queue */
    CSE_Semaphore results_slots;
    CSE_Semaphore results_items;
    /* Sempahore to signal the exit of all the worker threads */
    CSE_Semaphore workers_exit;
    /* Sempahore to signal the exit of all the waiting threads */
    CSE_Semaphore waiting_exit;
    /* Number of active worker threads */
    int workers;
    /* Number of waiting threads to retrieve data */
    int waiting;
    /* Flag to indicate that the workque has been destroyed*/
    char destroyed;
};

/* Initialize your workqueue here.  After this function returns, it
 * should be possible for:
 *  - Worker threads to join the queue
 *  - Work to be inserted in the queue
 *  - Results to be retrieved from the queue
 *
 * This function must allocate all resources necessary to manage the
 * queue.  As given, it simply allocates the WorkQueue object itself. */
WorkQueue workqueue_create(int slots) {
    if(slots <= 0)
        return NULL;
    WorkQueue wq = calloc(1, sizeof(struct WorkQueue));
    if(wq == NULL)
        return NULL;
    pthread_mutex_init(&(wq->lock),0);
    wq->work_slots = csesem_create(slots);
    if(wq->work_slots == NULL)
    {
        free(wq);
        return NULL;
    }
    wq->work_items = csesem_create(0);
    if(wq->work_items == NULL)
    {
        free(wq->work_slots);
        free(wq);
        return NULL;
    }
    wq->results_slots = csesem_create(slots);
    if(wq->results_slots == NULL)
    {
        free(wq->work_slots);
        free(wq->work_items);
        free(wq);
        return NULL;
    }
    wq->results_items = csesem_create(0);
    if(wq->results_items == NULL)
    {
        
        free(wq->work_slots);
        free(wq->work_items);
        free(wq->results_slots);
        free(wq);
        return NULL;
    }
    wq->workers_exit = csesem_create(1);
    if(wq->workers_exit == NULL)
    {
        free(wq->work_slots);
        free(wq->work_items);
        free(wq->results_slots);
        free(wq->results_items);
        free(wq);
        return NULL;
    }
    wq->waiting_exit = csesem_create(1);
    if(wq->waiting_exit == NULL)
    {
        free(wq->work_slots);
        free(wq->work_items);
        free(wq->results_slots);
        free(wq->results_items);
        free(wq->workers_exit);
        free(wq);
        return NULL;
    }
    wq->work = calloc(slots, sizeof(struct WorkItem));
    if(wq->work == NULL)
    {
        free(wq->results_items);
        free(wq->work_slots);
        free(wq->work_items);
        free(wq->results_slots);
        free(wq->workers_exit);
        free(wq->waiting_exit);
        free(wq);
        return NULL;
    }
    wq->results = calloc(slots,sizeof(void*));
    if(wq->results == NULL)
    {
        free(wq->work);
        free(wq->results_items);
        free(wq->work_slots);
        free(wq->work_items);
        free(wq->results_slots);
        free(wq->workers_exit);
        free(wq->waiting_exit);
        free(wq);
        return NULL;
    }
    wq->slots = slots;
    wq->results_front = 0;
    wq->results_rear = 0;
    wq->work_front = 0;
    wq->work_rear = 0;
    wq->destroyed = 0;
    wq->workers = 0;
    wq->waiting = 0;
    return wq;
}

/* This implementation is almost certainly insufficient for your work
 * queue; in particular, it makes assumptions about how you will manage
 * the state of your producer-consumer queues (that they will be
 * implemented exactly as laid out in the text) and it does not handle
 * workqueue destruction.  It should, however, give you an idea of how
 * worker threads are handled. */
void workqueue_work(WorkQueue wq) {
    int flag = 0;
    /* This thread should compute until the work queue is destroyed. */
    for (;;) {
        int index;
        WQ_Function func;
        void *data;

        /* This implementation inlines the producer-consumer queue
         * remove and insert functions (equivalent to the functions in
         * Figure 12.25 of your text).  You might want to make these
         * separate static functions, or implement them somehow entirely
         * differently.  It's up to you!  Notice that in this
         * implementation, wq->lock protects BOTH the work queue and the
         * results queue (that is, it plays the role of sbuf_t->mutex
         * from the text for both queues). */
        csesem_wait(wq->work_items);
        pthread_mutex_lock(&wq->lock);
        if(flag == 0)
        {
            wq->workers++;
            flag = 1;
            if(wq->workers == 1)
                csesem_wait(wq->workers_exit);
        }
        if(wq->destroyed)
        {
            wq->workers--;
            if(wq->workers == 0)
                 csesem_post(wq->workers_exit);
            pthread_mutex_unlock(&wq->lock);
            return;
        }
        /* Note that at this point we are GUARANTEED that there is at
         * least one available item, or wq->work_items would have been 0
         * and we would have blocked.
         *
         * The index manipulation here is somewhat different from the
         * manipulation in the text to avoid overflow effects.  It is
         * otherwise mathematically equivalent to line 37 of Figure
         * 12.25. */
        index = wq->work_front;
        wq->work_front = (wq->work_front + 1) % wq->slots;
        func = wq->work[index].func;
        data = wq->work[index].data;
        pthread_mutex_unlock(&wq->lock);
        csesem_post(wq->work_slots);

        /* Invoke the given work function on the provided data.  This
         * information should have been placed in the appropriate slot
         * by workqueue_insert(). */
        func(data);

        /* At this point, data has been (possibly) modified by func.
         * Insert the modified data on the results queue to be retrieved
         * by a call to workqueue_retrieve(). */
        csesem_wait(wq->results_slots);
        pthread_mutex_lock(&wq->lock);
        if(wq->destroyed)
        {
            wq->workers--;
            if(wq->workers == 0)
                 csesem_post(wq->workers_exit);
            pthread_mutex_unlock(&wq->lock);
            return;
        }
        index = wq->results_rear;
        wq->results_rear = (wq->results_rear + 1) % wq->slots;;
        wq->results[index] = data;
        pthread_mutex_unlock(&wq->lock);
        csesem_post(wq->results_items);

        /* At this point, a work item has been retrieved from the work
         * queue, processed, and its results placed on the result queue.
         * This iteration is finished, and we go back and wait for the
         * next work item. */
    }
}

void workqueue_insert(WorkQueue wq, WQ_Function func, void *data) {
    if(wq == NULL)
        return;
    int index;
    struct WorkItem w;
    w.func = func;
    w.data = data;
    csesem_wait(wq->work_slots);
    pthread_mutex_lock(&wq->lock);
    if(wq->destroyed)
    {
        pthread_mutex_unlock(&wq->lock);
        return;
    }
    wq->waiting++;
    if(wq->waiting == 1)
        csesem_wait(wq->waiting_exit);
    index = wq->work_rear;
    wq->work[index] = w;
    wq->work_rear = (wq->work_rear + 1)%wq->slots;
    pthread_mutex_unlock(&wq->lock);
    csesem_post(wq->work_items);
}

void *workqueue_retrieve(WorkQueue wq) {
    if(wq == NULL)
        return NULL;
    int index;
    void *data;
    csesem_wait(wq->results_items);
    pthread_mutex_lock(&wq->lock);
    if(wq->destroyed)
    {
        wq->waiting--;
        if(wq->waiting == 0)
             csesem_post(wq->waiting_exit);
        pthread_mutex_unlock(&wq->lock);
        return NULL;
    }
    wq->waiting--;
    if(wq->waiting == 0)
        csesem_post(wq->waiting_exit);
    index = wq->results_front;
    data = wq->results[index];
    wq->results_front = (wq->results_front + 1)%wq->slots;
    pthread_mutex_unlock(&wq->lock);
    csesem_post(wq->results_slots);
    return data;
}

/* The given implementation simply immediately frees the wq object.
 * This is CERTAINLY NOT CORRECT.  This function should notify all
 * worker threads that the queue is being destroyed, wait for them to
 * exit, then notify all waiting retrievals that there will be no more
 * results, wait for them to drain, and clean up all of the state for
 * this object.  (Destroy semaphores, free any allocated data, etc.).
 *
 * Consider what information you might need to achieve this.  Things like:
 *  - A count of active workers
 *  - A count of waiting retrievals
 *  - A flag to indicate that destruction is under way
 *  - A condition variable to signal readines
 *  - ... */
void workqueue_destroy(WorkQueue wq) {
    int i;
    pthread_mutex_lock(&wq->lock);
    wq->destroyed = 1;
    for(i = 0; i < wq->workers; i++)
    {
        csesem_post(wq->work_items);
        csesem_post(wq->results_slots);
    }
    for(i = 0; i < wq->waiting; i++)
    {
        csesem_post(wq->results_slots);
    }
    pthread_mutex_unlock(&wq->lock);
    csesem_wait(wq->waiting_exit);
    csesem_wait(wq->workers_exit);
    csesem_destroy(wq->work_items);
    csesem_destroy(wq->work_slots);
    csesem_destroy(wq->results_slots);
    csesem_destroy(wq->results_slots);
    csesem_destroy(wq->waiting_exit);
    csesem_destroy(wq->workers_exit);
    free(wq->results);
    free(wq->work);
    pthread_mutex_destroy(&wq->lock);
    free(wq);
}