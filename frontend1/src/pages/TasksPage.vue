<script setup>
import { onMounted, ref } from 'vue'

const tasks = ref([])
const error = ref(null)

const title = ref('')
const description = ref('')
const dueDate = ref('')

const fetchTasks = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/tasks', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      throw new Error('Failed to fetch tasks')
    }

    tasks.value = await response.json()
  } catch (err) {
    error.value = err.message
  }
}

const addTask = async () => {
  try {
    const token = localStorage.getItem('token')
    const API_URL = import.meta.env.VITE_API_URL;
    const response = await fetch(`${API_URL}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        title: title.value,
        description: description.value,
        due_date: dueDate.value || null
      })
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.error || 'Failed to add task')
    }

    
    title.value = ''
    description.value = ''
    dueDate.value = ''

    await fetchTasks() 
  } catch (err) {
    error.value = err.message
  }
}

const deleteTask = async (taskId) => {
  try {
    const token = localStorage.getItem('token')
    const API_URL = import.meta.env.VITE_API_URL;
    const response = await fetch(`${API_URL}/tasks/${taskId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      throw new Error('Failed to delete task')
    }

    await fetchTasks() 
  } catch (err) {
    error.value = err.message
  }
}

const editTaskId = ref(null)
const editTitle = ref('')
const editDescription = ref('')
const editDueDate = ref('')
const editError = ref('')


const startEdit = (task) => {
  editTaskId.value = task.id
  editTitle.value = task.title
  editDescription.value = task.description
  editDueDate.value = task.due_date || ''
  editError.value = ''
}

const cancelEdit = () => {
  editTaskId.value = null
  editError.value = ''
}

const saveEdit = async () => {
  if (!editTitle.value.trim()) {
    editError.value = 'Title is required'
    return
  }
  try {
    const token = localStorage.getItem('token')
    const API_URL = import.meta.env.VITE_API_URL;
    const response = await fetch(`${API_URL}/tasks/${editTaskId.value}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        title: editTitle.value,
        description: editDescription.value,
        due_date: editDueDate.value
      })
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.error || 'Failed to update task')
    }

    editTaskId.value = null
    await fetchTasks()
  } catch (err) {
    editError.value = err.message
  }
}

const toggleCompleted = async (task) => {
  try {
    const token = localStorage.getItem('token')
    const API_URL = import.meta.env.VITE_API_URL;
    const response = await fetch(`${API_URL}/tasks/${task.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        completed: !task.completed
      })
    })

    if (!response.ok) {
      throw new Error('Failed to update task status')
    }

    await fetchTasks()
  } catch (err) {
    error.value = err.message
  }
}


const logout = () => {
  localStorage.removeItem('token')
  window.location.href = '/login'
}




onMounted(fetchTasks)
</script>

<template>
    <div style="text-align: right; margin-bottom: 1rem;">
        <button @click="logout" class="logout-btn">Logout</button>
    </div>

    <div class="task-container">
      <h2>Your Tasks</h2>
  
      <div v-if="error" class="error">{{ error }}</div>

      <div class="add-task-form">
        <h3>Add New Task</h3>
            <input v-model="title" placeholder="Task title" class="add-input" />
            <input v-model="description" placeholder="Task description" class="add-input" />
            <input v-model="dueDate" type="date" class="add-input" />
            <button @click="addTask" class="add-btn">Add Task</button>
      </div>
  
      <transition-group v-if="tasks.length" name="fade" tag="ul" class="task-list">
        <li v-for="task in tasks" :key="task.id" class="task-item" :class="task.completed ? 'completed' : 'pending'">
          <div v-if="editTaskId === task.id" class="modal-overlay">
            <div class="modal">
              <h3>Edit Task</h3>
              <label>
                Title:
                <input v-model="editTitle" />
              </label>
              <label>
                Description:
                  <textarea v-model="editDescription" />
              </label>
              <label>
                Due Date:
                <input type="date" v-model="editDueDate" />
              </label>
              <p class="error" v-if="editError">{{ editError }}</p>
                <button @click="saveEdit">Save</button>
                <button @click="cancelEdit">Cancel</button>
            </div>
          </div>
          <div v-else class="task-left">
            <input 
              type="checkbox" 
              :checked="task.completed" 
              @change="toggleCompleted(task)"
          />
          <div class="task-details">
            <p class="task-title" :class="{ completed: task.completed }">{{ task.title }}</p>
            <p class="task-meta">{{ task.description }} | {{ task.due_date || 'No Due Date' }}</p>
          </div>
        </div>
        <div v-if="editTaskId !== task.id" class="task-actions">
          <button @click="startEdit(task)" class="edit-btn">Edit</button>
          <button @click="deleteTask(task.id)" class="delete-btn">Delete</button>
        </div>
      </li>

    </transition-group>
    
    </div>
  </template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.task-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 1.5rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.task-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f9f9f9;
  border-left: 5px solid transparent; /* new */
  border-radius: 8px;
  margin-bottom: 1rem;
  padding: 1rem;
  transition: background 0.3s, transform 0.2s;
}

.task-item.completed {
  border-left-color: #52c41a; /* green for completed */
  background-color: #f6ffed;
}

.task-item.pending {
  border-left-color: #faad14; /* orange for pending */
}


.task-item:hover {
  background: #f0f0f0;
}

.task-left {
  display: flex;
  align-items: center;
}

.task-details {
  margin-left: 1rem;

}

.task-title {
  font-weight: bold;
  margin: 0;
  font-size: 1.1rem;
}

.task-title.completed {
  text-decoration: line-through;
  color: #999;
}

.task-meta {
  font-size: 0.85rem;
  color: #666;
  margin-top: 0.2rem;
}

.task-actions button {
  margin-left: 0.5rem;
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.edit-btn {
  background-color: #ffe58f;
  color: #000;
}

.delete-btn {
  background-color: #ffa39e;
  color: white;
  transition: transform 0.2s ease, background-color 0.3s ease;
}

.delete-btn:hover {
  background-color: #ff7875;
  transform: scale(1.05) rotate(-2deg);
}


.error {
  color: red;
  margin-bottom: 1rem;
}

.edit-input {
  display: block;
  margin-bottom: 0.5rem;
  padding: 0.4rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  width: 100%;
  font-size: 0.95rem;
}

.save-btn {
  background-color: #95de64;
  color: white;
}

.cancel-btn {
  background-color: #d9d9d9;
  color: #333;
}

.add-task-form {
  margin-bottom: 2rem;
  padding: 1rem;
  background: #e6f7ff;
  border-radius: 10px;
}

.add-input {
  display: block;
  width: 100%;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.add-btn {
  background-color: #40a9ff;
  color: white;
  font-weight: bold;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.logout-btn {
  background-color: #d9d9d9;
  color: #333;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

.logout-btn:hover {
  background-color: #bfbfbf;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.modal label {
  display: block;
  margin-bottom: 1rem;
  font-weight: 600;
}

.modal input,
.modal textarea {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.3rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

.modal textarea {
  resize: vertical;
  min-height: 80px;
}

.modal button {
  margin-right: 1rem;
  padding: 0.6rem 1.2rem;
  font-weight: bold;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.modal button:first-of-type {
  background-color: #52c41a;
  color: white;
}

.modal button:last-of-type {
  background-color: #f5222d;
  color: white;
}

.error {
  color: #f5222d;
  margin-bottom: 1rem;
  font-weight: 600;
}


</style>

  
