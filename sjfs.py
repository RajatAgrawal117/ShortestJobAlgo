
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import base64


class SJFScheduler:
    def __init__(self, arrival_time, burst_time):
        self.total_processes = len(arrival_time)
        self.proc = []
        for i in range(self.total_processes):
            self.proc.append([arrival_time[i], burst_time[i], i + 1])
        
        self.proc = sorted(self.proc, key=lambda x: (x[0], x[1]))

        self.waiting_time = [0] * self.total_processes
        self.turnaround_time = [0] * self.total_processes
        self.start_time = [0] * self.total_processes
        self.complete_time = [0] * self.total_processes

    def schedule(self):
        service = [0] * self.total_processes
        service[0] = self.proc[0][0]
        self.waiting_time[0] = 0

        for i in range(1, self.total_processes):
            service[i] = service[i - 1] + self.proc[i - 1][1]
            self.waiting_time[i] = service[i] - self.proc[i][0]
            if self.waiting_time[i] < 0:
                self.waiting_time[i] = 0

        for i in range(self.total_processes):
            self.turnaround_time[i] = self.proc[i][1] + self.waiting_time[i]

        self.start_time[0] = self.proc[0][0]
        self.complete_time[0] = self.start_time[0] + self.turnaround_time[0]

        for i in range(1, self.total_processes):
            self.start_time[i] = self.complete_time[i - 1]
            self.complete_time[i] = self.start_time[i] + self.turnaround_time[i]

        process_data = []
        for i in range(self.total_processes):
            process_data.append([self.proc[i][2], self.start_time[i], self.complete_time[i], self.turnaround_time[i], self.waiting_time[i]])

        df = pd.DataFrame(process_data, columns=["Process_no", "Start_time", "Complete_time", "Turn_Around_Time", "Waiting_Time"])
        avg_tat = sum(self.turnaround_time) / self.total_processes
        avg_waiting_time = sum(self.waiting_time) / self.total_processes

        print("Process Details:")
        print(df)
        print("Average Turnaround Time: ", avg_tat)
        print("Average Waiting Time: ", avg_waiting_time)

        return df, avg_tat, avg_waiting_time

# Example usage:
# arrival_time_list = [0, 1, 2, 3]
# burst_time_list = [3, 4, 2, 5]
# sjf_scheduler = SJFScheduler(arrival_time_list, burst_time_list)
# df, avg_tat, avg_waiting_time = sjf_scheduler.schedule()

def main():
    st.title("Shortest Job First (SJF) Scheduling Algorithm")
    st.write("Enter task details below:")

    task_count = st.number_input("Number of tasks", min_value=1, step=1, value=3)
    arrival_time_list = []
    burst_time_list = []
    
    for i in range(task_count):
        task_id = i + 1
        arrival_time = st.number_input(f"Arrival time for Task {task_id}", step=1, value=0)
        burst_time = st.number_input(f"Burst time for Task {task_id}", step=1, value=1)
        arrival_time_list.append(arrival_time)
        burst_time_list.append(burst_time)

    scheduler = SJFScheduler(arrival_time_list, burst_time_list)

    # Perform scheduling
    # Add code to call SJFScheduler methods and get results
    df, avg_waiting_time, avg_turnaround_time = scheduler.schedule()

    # Display results
    st.write("Task scheduling results:")
    st.write(df)
    st.write("Average Turnaround Time:", avg_turnaround_time)
    st.write("Average Waiting Time:", avg_waiting_time)

    # Visualize scheduling process using a bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    task_names = [f"Task {i+1}\n(Arrival: {arrival}, Burst: {burst})" for i, (arrival, burst) in enumerate(zip(arrival_time_list, burst_time_list))]
    waiting_bars = ax.bar(task_names, df["Waiting_Time"], label="Waiting Time")
    turnaround_bars = ax.bar(task_names, df["Turn_Around_Time"] - df["Waiting_Time"], bottom=df["Waiting_Time"], label="Turn Around Time")
    ax.set_xlabel("Task")
    ax.set_ylabel("Time")
    ax.set_title("Task Scheduling Process")
    ax.legend()
    plt.xticks(rotation=45, ha='right')

    # Add labels for each bar
    for bar in waiting_bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    for bar in turnaround_bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height + bar.get_y()),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    st.pyplot(fig)

if __name__ == "__main__":
    main()
