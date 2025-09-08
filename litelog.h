#ifndef LITELOG_H
#define LITELOG_H

#include <stddef.h>
#include <time.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define LOG_LEVEL uint32_t
#define LOG_LEVEL_INFO (0U)
#define LOG_LEVEL_WARNING (1U)
#define LOG_LEVEL_ERROR (2U)
#define LOG_LEVEL_FATAL (3U)
#define LOG_LEVEL_ALL (4U)

// user-defined assignees
#define ASSIGNEE uint32_t
#define ASSIGNEE_HYAM (0U)
#define ASSIGNEE_JAY (1U)
#define ASSIGNEE_SK (2U)
#define ASSIGNEE_RAY (3U)
#define ASSIGNEE_ALL (4U)
// -----------------------

// user-defined log structure
#define EVENT_TYPE_MSG (0U)
struct event_type_msg
{
    char msg[32];
};

#define EVENT_TYPE_ALL (1U)
// -----------------------

// log entry structure
struct log_entry
{
    time_t timestamp; // 4B

    uint32_t level : 2;
    uint32_t assignee : 6;
    uint32_t data_size : 24; // 4B, max to 16MB

    void *data; // 4B
};

bool open_log(char *file_name, size_t file_size);
bool save_log(char *file_name);
bool add_log(LOG_LEVEL level, ASSIGNEE assignee, void *data, size_t data_size);

bool add_log(LOG_LEVEL level, ASSIGNEE assignee, void *data, size_t data_size)
{
    // check parameters
    if (data == NULL || data_size == 0 || data_size >= (1 << 24) ||
        level >= LOG_LEVEL_ALL || assignee >= ASSIGNEE_ALL)
    {
        return false;
    }

    // create log entry
    struct log_entry entry;
    entry.timestamp = time(NULL);
    entry.level = level;
    entry.assignee = assignee;
    entry.data_size = data_size;
    entry.data = data;

    return true;
}

#endif