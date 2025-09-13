#include "litelog.h"

int main()
{
    remove_log(); // remove existing log file for clean test

    LOG_DATA_EXAMPLE1 example1 = {
        .cpu_usage = 45,
        .mem_usage = 30,
        .thread_count = 5}; // example values
    ADD_LOG(LOG_LEVEL_WARNING, LOG_DATA_TYPE_EXAMPLE1, LOG_ACTION_NONE, &example1, LOG_DATA_TYPE_EXAMPLE1_SIZE);

    LOG_DATA_EXAMPLE2 example2 = {
        .src_ip = "10.0.0.1",
        .dst_ip = "8.8.8.8",
        .port = 8080}; // example values
    ADD_LOG(LOG_LEVEL_ERROR, LOG_DATA_TYPE_EXAMPLE2, LOG_ACTION_NONE, &example2, LOG_DATA_TYPE_EXAMPLE2_SIZE);

    LOG_DATA_EXAMPLE3 example3 = {
        .name = "TestUser",
        .level = 1}; // example values
    ADD_LOG(LOG_LEVEL_FATAL, LOG_DATA_TYPE_EXAMPLE3, LOG_ACTION_NONE, &example3, LOG_DATA_TYPE_EXAMPLE3_SIZE);

    LOG_DATA_MSG msg = {
        .msg = "This is a test log message.\n\r"};
    ADD_LOG(LOG_LEVEL_INFO, LOG_DATA_TYPE_MSG, LOG_ACTION_SAVE_NOW, &msg, LOG_DATA_TYPE_MSG_SIZE);
    return 0;
}