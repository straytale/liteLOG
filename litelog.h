#ifndef LITELOG_H
#define LITELOG_H

#include <stddef.h>
#include <time.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// user-define configurations
#define MAX_LOG_ENTRIES (1024U) // when entrys exceed this, auto save will be triggered
#define LOG_FILE_NAME "log.bin"

// user-defined log levels
#define LOG_LEVEL uint16_t
#define LOG_LEVEL_INFO (0U)
#define LOG_LEVEL_WARNING (1U)
#define LOG_LEVEL_ERROR (2U)
#define LOG_LEVEL_FATAL (3U)
#define LOG_LEVEL_ALL (4U)

// user-defined log data types
#define LOG_DATA_TYPE uint16_t
#define LOG_DATA_TYPE_MSG (0U)
#define LOG_DATA_TYPE_EXAMPLE1 (1U)
#define LOG_DATA_TYPE_EXAMPLE2 (2U)
#define LOG_DATA_TYPE_EXAMPLE3 (3U)
#define LOG_DATA_TYPE_ALL (4U)

// user-defined data structure
typedef struct
{
    char msg[64];
} LOG_DATA_MSG, *LOG_DATA_MSG_PTR;
#define LOG_DATA_TYPE_MSG_SIZE (sizeof(LOG_DATA_MSG))

typedef struct
{
    uint16_t cpu_usage; // MAX to 0x64
    uint16_t mem_usage; // MAX to 0x64
    uint32_t thread_count;
} LOG_DATA_EXAMPLE1, *LOG_DATA_EXAMPLE1_PTR;
#define LOG_DATA_TYPE_EXAMPLE1_SIZE (sizeof(LOG_DATA_EXAMPLE1))

typedef struct
{
    char src_ip[16];
    char dst_ip[16];
    uint16_t port;
} LOG_DATA_EXAMPLE2, *LOG_DATA_EXAMPLE2_PTR;
#define LOG_DATA_TYPE_EXAMPLE2_SIZE (sizeof(LOG_DATA_EXAMPLE2))

typedef struct
{
    char name[32];
    uint16_t level;
} LOG_DATA_EXAMPLE3, *LOG_DATA_EXAMPLE3_PTR;
#define LOG_DATA_TYPE_EXAMPLE3_SIZE (sizeof(LOG_DATA_EXAMPLE3))

// ----------------------------------------------------------------

// log entry structure
typedef struct
{
    uint32_t timestamp;
    uint16_t level;
    uint16_t type;
    uint32_t data_size;
    void *data; // 4B
} LOG_ENTRY, *LOG_ENTRY_PTR;

LOG_ENTRY log_entries[MAX_LOG_ENTRIES];
static uint32_t entry_index = 0U; // current log entry index

// actions
#define LOG_ACTION uint16_t
#define LOG_ACTION_NONE (0U)     // when entries are allocated, log will be auto saved
#define LOG_ACTION_SAVE_NOW (1U) // trigger save action
#define LOG_ACTION_ALL (2U)

#define ADD_LOG(level, type, action, data, data_size) \
    add_log(level, type, action, data, data_size)

/**
 *  @brief Add a log entry
 *  @param level Log level (user-defined)
 *  @param type Log data type (user-defined)
 *  @param action Log action (none or save_now)
 *  @param data Pointer to log data
 *  @param data_size Size of log data
 *  @return true if log entry is added successfully, false otherwise
 */
bool add_log(LOG_LEVEL level, LOG_DATA_TYPE type, LOG_ACTION action, void *data, uint32_t data_size)
{
    // check parameters
    if (level >= LOG_ACTION_ALL || type >= LOG_DATA_TYPE_ALL || action >= LOG_ACTION_ALL)

    {
        return false;
    }

    // create log entry
    LOG_ENTRY_PTR entry_ptr = &log_entries[entry_index];
    entry_ptr->timestamp = time(NULL);
    entry_ptr->level = level;
    entry_ptr->type = type;
    entry_ptr->data_size = data_size;
    entry_ptr->data = malloc(data_size);
    memcpy(entry_ptr->data, data, data_size);

    // increment entry index
    entry_index++;

    // save log entries to file if needed
    if (entry_index >= MAX_LOG_ENTRIES || action == LOG_ACTION_SAVE_NOW)
    {
        // save log entries to file
        FILE *file = fopen(LOG_FILE_NAME, "ab");
        if (file == NULL)
        {
            return false;
        }
        fwrite(log_entries, sizeof(LOG_ENTRY), entry_index, file);
        fclose(file);

        // free allocated memory
        for (uint32_t i = 0; i < entry_index; i++)
        {
            free(log_entries[i].data);
            log_entries[i].data = NULL;
        }
        entry_index = 0U;
    }

    return true;
}

#endif