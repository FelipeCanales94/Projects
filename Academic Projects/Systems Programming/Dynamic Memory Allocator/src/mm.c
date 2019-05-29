#include <unistd.h>
#include <string.h>


/* When requesting memory from the OS using sbrk(), request it in
 * increments of CHUNK_SIZE. */
#define CHUNK_SIZE (1<<14)
/*
 * Macros based on example provided in:
 * Computer Systems. A Programmer's Perspective. Bryant and O'Hallaron.
 * Second Edition. 2011. Prentice Hall.
 */

#ifndef MACROSH_H
#define MACROSH_H
/*
 * Macros based on example provided in:
 * Computer Systems. A Programmer's Perspective. Bryant and O'Hallaron.
 * Second Edition. 2011. Prentice Hall.
 */


/* Basic constants and macros */
#define WSIZE 8
/* Word and header/footer size (bytes) */
#define DSIZE 16
/* Double word size (bytes) */
#define MAX_BLOCK_SIZE (1<<11)
/* Extend heap by this amount (bytes) */
#define MAX(x, y) ((x) > (y)? (x) : (y))
/* Pack a size and allocated bit into a word */
#define PACK(size, alloc)  ((size) | (alloc))
/* Read and write a word at address p */
#define GET(p) (*(unsigned long long *)(p))
#define PUT(p, val)  (*(unsigned long long *)(p) = (val))
/* Read the size and allocated fields from address p */
#define GET_SIZE(p)  ((*(unsigned long long *)(p)) & (unsigned long long)(~0x7))

#define GET_ALLOC(p) ((*(unsigned long long *)(p)) & (unsigned long long)(0x1))
/* Given block ptr bp, compute address of its header and footer */
#define HDRP(bp) ((char *)(bp) - WSIZE)
#define FTRP(bp) ((char *)(bp) + GET_SIZE(HDRP(bp)) - DSIZE)
/* Given block ptr bp, compute address of next and previous blocks */
#define NEXT_BLKP(bp)  (char *)(bp) + GET_SIZE((char *)(bp) - WSIZE)
#define PREV_BLKP(bp)  (char *)(bp) - GET_SIZE((char *)(bp) - DSIZE)


#endif
/* Private global variables */
static char *heap_listp = NULL;                            /* Points to first byte of heap */

/* Max legal heap addr plus 1*/
/*
 * This function, defined in bulk.c, allocates a contiguous memory
 * region of at least size bytes.  It MAY NOT BE USED as the allocator
 * for buddy-allocated regions.  Memory allocated using bulk_alloc()
 * must be freed by bulk_free().
 *
 * This function will return NULL on failure.
 */
extern void *bulk_alloc(size_t size);

/*
 * This function is also defined in bulk.c, and it frees an allocation
 * created with bulk_alloc().  Note that the pointer passed to this
 * function MUST have been returned by bulk_alloc(), and the size MUST
 * be the same as the size passed to bulk_alloc() when that memory was
 * allocated.  Any other usage is likely to fail, and may crash your
 * program.
 */
extern void bulk_free(void *ptr, size_t size);

/*
 * This function computes the log base 2 of the buddy block size for a
 * given allocation.  To find the buddy block size from the result of
 * this function, use 2 << block_size(x).
 *
 * Note that its results are NOT meaningful for any
 * size > 2024!
 */
static inline __attribute__((unused)) int block_size(size_t x) {
    if (x == 0) {
        return 5;
    } else {
        return 32 - __builtin_clz((unsigned int)x + 15);
    }
}

static void *coalesce(void *bp)
{
    unsigned long long prev_alloc = GET_ALLOC(HDRP(PREV_BLKP(bp)));
    unsigned long long next_alloc = GET_ALLOC(HDRP(NEXT_BLKP(bp)));
    size_t size = GET_SIZE(HDRP(bp));
    if(size >=2048)
        return bp;
    if (prev_alloc && next_alloc) {                                   /* Case 1 */
        return bp;
    }
    else if (prev_alloc && !next_alloc) {                             /* Case 2 */
        size_t next_size = GET_SIZE(HDRP(NEXT_BLKP(bp)));
        if(next_size != size)
            return bp;
        size <<=1;
        PUT(HDRP(bp), PACK(size,0));
        PUT(FTRP(bp), PACK(size,0));
    }
    else if (!prev_alloc && next_alloc) {                             /* Case 3 */
        size_t prev_size = GET_SIZE(HDRP(PREV_BLKP(bp)));
        if(prev_size != size)
            return bp;
        size <<=1;
        PUT(FTRP(bp), PACK(size, 0));
        PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));
        bp = PREV_BLKP(bp);
    }
    else {                                                            /* Case 4 */
        size_t next_size = GET_SIZE(HDRP(NEXT_BLKP(bp)));
        size_t prev_size = GET_SIZE(HDRP(PREV_BLKP(bp)));
        if(size == next_size)
        {
            size <<=1;
            PUT(HDRP(bp), PACK(size,0));
            PUT(FTRP(bp), PACK(size,0));
            if(size == prev_size)
            {
                size <<=1;
                PUT(FTRP(bp), PACK(size, 0));
                PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));
                bp = PREV_BLKP(bp);
            }
        }
        else if(size == prev_size )
        {
            size <<=1;
            PUT(FTRP(bp), PACK(size, 0));
            PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));
            bp = PREV_BLKP(bp);
            if(size == next_size)
            {
                size <<=1;
                PUT(HDRP(bp), PACK(size,0));
                PUT(FTRP(bp), PACK(size,0));
            }
        }
        else
            return bp;
    }
    return coalesce(bp);
}
/*
 * You should implement a free() that can successfully free a region of
 * memory allocated by any of the above allocation routines, whether it
 * is a buddy or block allocated region.
 *
 * The given implementation does nothing.
 */
void free(void *ptr){
    size_t size = GET_SIZE(HDRP(ptr));
    if(size>2048)
    {
        bulk_free(HDRP(ptr),size-WSIZE);
    }
    else
    {
        PUT(HDRP(ptr),PACK(size,0));
        PUT(FTRP(ptr),PACK(size,0));
        coalesce(ptr);
    }
}
static void place_begin(void *bp, size_t asize)
{
    size_t block_size;
    block_size =  GET_SIZE(HDRP(bp));
    while(block_size > 2*DSIZE && (block_size>>1) >=asize)
    {
        block_size >>=1;
        PUT(HDRP(bp+block_size), PACK(block_size,0));
        PUT(FTRP(bp+block_size),GET(HDRP(bp+block_size)));
        PUT(HDRP(bp), PACK(block_size,1));
        PUT(FTRP(bp),GET(HDRP(bp)));
        coalesce(bp+block_size);
    }

}
static void place_end(void *bp, size_t asize)
{
    size_t block_size;
    block_size =  GET_SIZE(HDRP(bp));
    while(block_size > 2*DSIZE && (block_size>>1) >=asize)
    {
        block_size >>=1;
        PUT(HDRP(bp), PACK(block_size,0));
        PUT(FTRP(bp),GET(HDRP(bp)));
        bp += block_size;
    }
    PUT(HDRP(bp),PACK(0,1));
    PUT(bp + 2*WSIZE,PACK(0,1));
}

static void *extend_heap(size_t words)
{
    void *bp;
    size_t size;
    /* Allocate an even number of words to maintain alignment */
    size = (words % 2) ? (words+1) * WSIZE : words * WSIZE;
    if ((bp = sbrk(size)) == (void *)-1)
        return NULL;
    return bp;
}

static int mm_init(void)
{
    int i;
    void *hp;
    /* Create the initial empty heap */
    if ((heap_listp = extend_heap(CHUNK_SIZE/WSIZE)) == (void *)-1)
        return -1;
    hp = heap_listp;
    for(i = 0; i< 8; i++)
    {
        PUT(hp, PACK(MAX_BLOCK_SIZE, 0));                                   /* Stablish header */
        PUT(hp + MAX_BLOCK_SIZE - WSIZE, PACK(MAX_BLOCK_SIZE, 0));          /* Stablish footer */
        hp += MAX_BLOCK_SIZE;
    }
    place_begin(heap_listp + WSIZE,2*DSIZE);                                 /* Split first block */
    hp -= MAX_BLOCK_SIZE - WSIZE;
    place_end(hp,2*DSIZE);                                                   /* Split last block */
    return 0;
}

static void *find_fit(size_t asize)
{
    void * current_block;
    void * best_fit = NULL;
    size_t best_size;
    size_t current_size;
    current_block = heap_listp+2*DSIZE;
    while((current_size = GET_SIZE(current_block))>0)
    {

        if(current_size >= asize && !GET_ALLOC(current_block))
        {
            if(best_fit == NULL || current_size<best_size)
            {
                best_size = current_size;
                best_fit = current_block + WSIZE;
            }
        }
        current_block = NEXT_BLKP(current_block+WSIZE)-WSIZE;
    }
    return best_fit;
}


/*
 * You must implement malloc().  Your implementation of malloc() must be
 * the buddy allocator described in the project handout.
 */
void *malloc(size_t size) {

    void *bp, *final_bp;
    int i;
    if(heap_listp == NULL)
        if(mm_init()!=0)
            return NULL;
    if(size<=0)
        return NULL;
    if(size > 2024)
    {
        size += WSIZE;
        bp = bulk_alloc(size);
        PUT(bp, PACK(size+WSIZE,1));
        return bp + WSIZE;
    }
    else
    {
        size = 1 << block_size(size);
        bp = find_fit(size);
        if(bp == NULL)
        {
            bp = extend_heap(CHUNK_SIZE/WSIZE);
            final_bp = bp;
            for(i = 0;i < 8; i++)
            {
                PUT(final_bp, PACK(MAX_BLOCK_SIZE, 0));                                   /* Stablish header */
                PUT(final_bp + MAX_BLOCK_SIZE - WSIZE, PACK(MAX_BLOCK_SIZE, 0));          /* Stablish footer */
                final_bp += MAX_BLOCK_SIZE;
            }
            final_bp -= MAX_BLOCK_SIZE - WSIZE;
            place_end(final_bp,2*DSIZE);                                                   /* Split last block */
            PUT(bp-WSIZE,PACK(2*DSIZE,1));                                          /* Remove the epilogue structure */
            PUT(bp - 4*WSIZE,PACK(2*DSIZE,1));
            free(PREV_BLKP(bp+WSIZE));
            bp = find_fit(size);
            if(bp == NULL)
                return NULL;
        }
        place_begin(bp, size);
        return bp;
    }
}

/*
 * You must also implement calloc().  It should create allocations
 * compatible with those created by malloc().  In particular, any
 * allocations of a total size <= 2024 bytes must be buddy allocated,
 * while larger allocations must use the bulk allocator.
 *
 * calloc() (see man 3 calloc) returns a cleared allocation large enough
 * to hold nmemb elements of size size.  It is cleared by setting every
 * byte of the allocation to 0.  You should use the function memset()
 * for this (see man 3 memset).
 */
void *calloc(size_t nmemb, size_t size) {
    void *ptr = malloc(nmemb * size);
    if(ptr == NULL)
        return NULL;
    memset(ptr, 0, nmemb * size);
    return ptr;
}

/*
 * You must also implement realloc().  It should create allocations
 * compatible with those created by malloc(), honoring the buddy
 * alocation and bulk allocation rules.  It must move data from the
 * previously-allocated block to the newly-allocated block if it cannot
 * resize the given block directly.  See man 3 realloc for more
 * information on what this means.
 *
 * It is not possible to implement realloc() using bulk_alloc() without
 * additional metadata, so the given code is NOT a working
 * implementation!
 */
void *realloc(void *ptr, size_t size) {
    void *next_block;
    if(size <= 0)
        return NULL;
    if(ptr == NULL)
    {
        return malloc(size);
    }
    else
    {
        size_t old_size = GET_SIZE(HDRP(ptr));
        size_t new_size = 1 << block_size(size);
        if(size > 2024)
        {
            next_block = malloc(size);
            memcpy(next_block,ptr, GET_SIZE(HDRP(ptr))-DSIZE);
            free(ptr);
            return next_block;
        }
        if(old_size < new_size)
        {
            place_begin(ptr,new_size);
            return ptr;
        }
        else
        {
            size_t difference = new_size - old_size;
            if(difference == 0)
                return ptr;
            next_block = NEXT_BLKP(ptr);
            while(old_size < new_size && !GET_ALLOC(next_block))
            {
                if(old_size == GET_SIZE(HDRP(next_block)))
                {
                    old_size <<= 1;
                }
                else
                {
                    break;
                }
                next_block = NEXT_BLKP(next_block);
            }
            if(old_size == new_size)
            {
                PUT(HDRP(ptr), PACK(new_size, 1));                                   /* Stablish header */
                PUT(FTRP(ptr), PACK(new_size, 1));
                return ptr;
            }
            else
            {
                next_block = malloc(size);
                if(next_block == NULL)
                {
                    return NULL;
                }
                else
                {
                    memcpy(next_block,ptr, GET_SIZE(HDRP(ptr))-DSIZE);
                    free(ptr);
                    return next_block;
                }
            }
        }
    }
}