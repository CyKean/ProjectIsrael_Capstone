<template>
      <div class="flex-1 w-full px-4 sm:px-6 lg:px-10 overflow-hidden">
        
        <!-- Main Container - Everything Inside -->
        <div class="bg-white rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-green-100 h-[calc(100vh-140px)] overflow-hidden">
          
          <!-- Header - Inside Main Container -->
          <div class="bg-gradient-to-r from-emerald-50 to-white p-6 border-b border-gray-100 rounded-t-lg">
            <h1 class="text-xl font-semibold text-gray-800 mb-1">User Profile</h1>
            <p class="text-emerald-600 mt-1 text-sm">Manage your account information and security settings</p>
          </div>

          <!-- Two Containers with Gap Inside Main Container -->
          <div class="flex gap-6 h-[calc(100%-100px)] p-6">
            
            <!-- Left Container - Profile Avatar (30% width) -->
            <div class="w-[30%] bg-gradient-to-br from-gray-50 to-gray-100 rounded-[16px] border border-gray-200 overflow-y-auto">
              <div class="px-3 py-6 flex flex-col items-center">
                
                <!-- Large Profile Circle -->
                <div class="mb-6 flex flex-col items-center">
                  <div class="relative">
                    <!-- Profile Avatar Circle -->
                    <div class="w-32 h-32 rounded-full bg-white shadow-xl border-4 border-emerald-200 flex items-center justify-center text-6xl transition-all duration-300 hover:scale-105 hover:shadow-2xl mb-4">
                      {{ selectedAvatar.icon }}
                    </div>

                    <!-- Glow Effect -->
                    <div class="absolute inset-0 w-32 h-32 rounded-full bg-emerald-200 opacity-20 blur-xl -z-10"></div>
                  </div>

                  <!-- Avatar Name -->
                  <p class="text-center text-sm font-medium text-gray-800 mb-1">{{ selectedAvatar.name }}</p>
                  <div class="w-8 h-0.5 bg-emerald-400 rounded-full"></div>
                </div>

                <!-- Avatar Selection Section -->
                <div class="w-full max-w-full">
                  <div class="text-center mb-4">
                    <h3 class="text-sm font-semibold text-gray-900 mb-2">Choose Avatar</h3>
                    <div class="w-16 h-0.5 bg-gradient-to-r from-emerald-400 to-emerald-600 rounded-full mx-auto mb-4"></div>
                  </div>
                  
                  <!-- Avatar Grid -->
                  <div class="flex justify-center mb-4">
                    <div class="grid grid-cols-5 gap-4">
                      <div 
                        v-for="avatar in avatarOptions" 
                        :key="avatar.id"
                        @click="selectAvatar(avatar)"
                        :class="[ 
                          'w-14 h-14 rounded-full flex items-center justify-center text-xl cursor-pointer transition-all duration-200 border-2 bg-white shadow-sm hover:shadow-lg relative',
                          selectedAvatar.id === avatar.id 
                            ? 'border-emerald-500 bg-emerald-50 scale-110 shadow-lg ring-2 ring-emerald-200' 
                            : 'border-gray-200 hover:border-emerald-300 hover:scale-105'
                        ]"
                      >
                        {{ avatar.icon }}
                        
                        <!-- Selection indicator -->
                        <div 
                          v-if="selectedAvatar.id === avatar.id"
                          class="absolute -top-1 -right-1 w-3 h-3 bg-emerald-500 rounded-full flex items-center justify-center"
                        >
                          <CheckCircle class="w-2 h-2 text-white" />
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Instruction text -->
                  <div class="text-center bg-white/50 rounded-lg p-2 border border-gray-200 mx-1">
                    <p class="text-xs font-medium text-gray-600">Select your profile character</p>
                    <p class="text-xs text-gray-500 mt-1">Choose from {{ avatarOptions.length }} available options</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Container - Personal Info & Security (70% width) -->
            <div class="flex-1 bg-gradient-to-br from-white to-gray-50/30 rounded-[16px] border border-gray-200 overflow-y-auto">
              <div class="p-6">
                
                <!-- Personal Information Section -->
                <div class="mb-8">
                  <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300">
                    <!-- Header with Edit Button -->
                    <div class="flex items-center justify-between mb-6">
                      <div class="flex items-center">
                        <div class="w-10 h-10 bg-emerald-100 rounded-xl flex items-center justify-center mr-4">
                          <User class="w-5 h-5 text-emerald-600" />
                        </div>
                        <div>
                          <h3 class="text-base font-semibold text-gray-900">Personal Information</h3>
                          <p class="text-sm text-gray-500">Update your personal details</p>
                        </div>
                      </div>
                      
                      <!-- Edit Button with Tooltip -->
                      <div class="relative group">
                        <button
                          @click="toggleEditMode"
                          :class="[
                            'p-2 rounded-lg transition-all duration-200 flex items-center justify-center',
                            isEditMode 
                              ? 'bg-emerald-500 text-white hover:bg-emerald-600 shadow-md' 
                              : 'bg-emerald-100 text-emerald-600 hover:bg-emerald-200'
                          ]"
                          :title="isEditMode ? 'Cancel editing' : 'Update Profile'"
                        >
                          <Edit3 v-if="!isEditMode" class="w-4 h-4" />
                          <X v-else class="w-4 h-4" />
                        </button>
                        
                        <!-- Tooltip -->
                        <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
                          {{ isEditMode ? 'Cancel editing' : 'Update Profile' }}
                          <div class="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-2 border-r-2 border-t-2 border-transparent border-t-gray-800"></div>
                        </div>
                      </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <!-- Full Name -->
                      <div class="space-y-2">
                        <label class="text-sm font-medium text-gray-700">Full Name</label>
                        <div class="relative group">
                          <User class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 group-focus-within:text-emerald-500 transition-colors duration-200" />
                          <input 
                            v-model="profileData.name"
                            @input="onFieldChange"
                            type="text"
                            :disabled="!isEditMode"
                            :class="[
                              'w-full pl-10 pr-4 py-3 border rounded-xl transition-all duration-200',
                              isEditMode 
                                ? 'border-gray-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent bg-white hover:border-gray-300' 
                                : 'border-gray-100 bg-gray-50 text-gray-600 cursor-not-allowed'
                            ]"
                            placeholder="Enter your full name"
                          />
                        </div>
                      </div>

                      <!-- Phone Number -->
                      <div class="space-y-2">
                        <label class="text-sm font-medium text-gray-700">Phone Number</label>
                        <div class="relative group">
                          <Phone class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 group-focus-within:text-emerald-500 transition-colors duration-200" />
                          <input 
                            v-model="profileData.phone"
                            @input="onFieldChange"
                            type="tel"
                            :disabled="!isEditMode"
                            :class="[
                              'w-full pl-10 pr-4 py-3 border rounded-xl transition-all duration-200',
                              isEditMode 
                                ? 'border-gray-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent bg-white hover:border-gray-300' 
                                : 'border-gray-100 bg-gray-50 text-gray-600 cursor-not-allowed'
                            ]"
                            placeholder="Enter your phone number"
                          />
                        </div>
                      </div>
                    </div>

                    <!-- Save Button -->
                    <div class="mt-6">
                      <button 
                        @click="saveProfile"
                        :disabled="!canSave || isLoadingProfile"
                        :class="[
                          'px-6 py-2.5 rounded-xl font-medium shadow-lg transition-all duration-200 flex items-center',
                          canSave && !isLoadingProfile
                            ? 'bg-gradient-to-r from-emerald-500 to-emerald-600 text-white hover:from-emerald-600 hover:to-emerald-700 hover:shadow-xl transform hover:-translate-y-0.5 cursor-pointer'
                            : 'bg-gray-300 text-gray-500 cursor-not-allowed opacity-70'
                        ]"
                      >
                        <CheckCircle class="w-4 h-4 mr-2" />
                        {{ isLoadingProfile ? 'Saving...' : 'Save Changes' }}
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Security Settings Section -->
                <div class="mb-8">
                  <div class="flex items-center mb-6">
                    <div class="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center mr-4">
                      <Shield class="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                      <h3 class="text-base font-semibold text-gray-900">Security Settings</h3>
                      <p class="text-sm text-gray-500">Manage your account security</p>
                    </div>
                  </div>
                  
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    
                    <!-- Reset Password Card -->
                    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden group">
                      <div class="p-5">
                        <div class="flex items-center mb-4">
                          <div class="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center mr-3 group-hover:bg-blue-200 transition-colors duration-200">
                            <Lock class="w-5 h-5 text-blue-600" />
                          </div>
                          <div>
                            <h4 class="text-sm font-semibold text-gray-900">Change Password</h4>
                            <p class="text-xs text-gray-500">Update your account password</p>
                          </div>
                        </div>
                        
                        <!-- Show Get Started button only when form is not visible -->
                        <button 
                          v-if="!showPasswordSection"
                          @click="togglePasswordSection"
                          :disabled="isPasswordDisabled || isLoadingPassword"
                          class="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-2.5 px-4 rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all duration-200 text-sm font-medium shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-not-allowed"
                        >
                          {{ isLoadingPassword ? 'Updating...' : (isPasswordDisabled ? 'Password login not active' : 'Get Started') }}
                        </button>
                        
                        <!-- Password Form with Show/Hide and TOP BORDER LINE -->
                        <div 
                          v-if="showPasswordSection"
                          class="mt-4 pt-4 border-t border-gray-100"
                        >
                          <div class="space-y-3">
                            <div>
                              <label class="block text-xs font-medium text-gray-700 mb-1">Current Password</label>
                              <div class="relative flex items-center">
                                <input 
                                  :type="showCurrentPassword ? 'text' : 'password'"
                                  v-model="passwordForm.current"
                                  class="w-full px-3 py-2 pr-10 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-sm"
                                  placeholder="Enter current password"
                                />
                                <button
                                  type="button"
                                  @click="showCurrentPassword = !showCurrentPassword"
                                  class="absolute right-3 inset-y-0 my-auto flex items-center justify-center text-gray-400 hover:text-gray-600 transition-colors duration-200 z-10"
                                >
                                  <Eye v-if="!showCurrentPassword" class="w-4 h-4" />
                                  <EyeOff v-else class="w-4 h-4" />
                                </button>
                              </div>
                            </div>
                            <div>
                              <label class="block text-xs font-medium text-gray-700 mb-1">New Password</label>
                              <div class="relative flex items-center">
                                <input 
                                  :type="showNewPassword ? 'text' : 'password'"
                                  v-model="passwordForm.new"
                                  class="w-full px-3 py-2 pr-10 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-sm"
                                  placeholder="Enter new password"
                                />
                                <button
                                  type="button"
                                  @click="showNewPassword = !showNewPassword"
                                  class="absolute right-3 inset-y-0 my-auto flex items-center justify-center text-gray-400 hover:text-gray-600 transition-colors duration-200 z-10"
                                >
                                  <Eye v-if="!showNewPassword" class="w-4 h-4" />
                                  <EyeOff v-else class="w-4 h-4" />
                                </button>
                              </div>
                            </div>
                            <div>
                              <label class="block text-xs font-medium text-gray-700 mb-1">Confirm Password</label>
                              <div class="relative flex items-center">
                                <input 
                                  :type="showConfirmPassword ? 'text' : 'password'"
                                  v-model="passwordForm.confirm"
                                  class="w-full px-3 py-2 pr-10 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-sm"
                                  placeholder="Confirm new password"
                                />
                                <button
                                  type="button"
                                  @click="showConfirmPassword = !showConfirmPassword"
                                  class="absolute right-3 inset-y-0 my-auto flex items-center justify-center text-gray-400 hover:text-gray-600 transition-colors duration-200 z-10"
                                >
                                  <Eye v-if="!showConfirmPassword" class="w-4 h-4" />
                                  <EyeOff v-else class="w-4 h-4" />
                                </button>
                              </div>
                            </div>
                          </div>
                          
                          <!-- Buttons Section with spacing -->
                          <div class="space-y-3 mt-4">
                            <!-- Update Password Button -->
                            <button 
                              @click="changePassword"
                              :disabled="isLoadingPassword"
                              class="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-2 px-4 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-200 text-sm font-medium disabled:opacity-70 disabled:cursor-not-allowed"
                            >
                              {{ isLoadingPassword ? 'Updating...' : 'Update Password' }}
                            </button>
                            
                            <!-- Cancel Button -->
                            <button 
                              @click="togglePasswordSection"
                              class="w-full bg-gradient-to-r from-blue-300 to-blue-400 text-gray-700 font-semibold py-2 px-4 rounded-lg hover:from-blue-400 hover:to-blue-500 transition-all duration-200 text-sm font-medium"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Reset Pin Code Card -->
                    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden group">
                      <div class="p-5">
                        <div class="flex items-center mb-4">
                          <div class="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center mr-3 group-hover:bg-purple-200 transition-colors duration-200">
                            <Shield class="w-5 h-5 text-purple-600" />
                          </div>
                          <div>
                            <h4 class="text-sm font-semibold text-gray-900">Change Pin Code</h4>
                            <p class="text-xs text-gray-500">Update your security pin</p>
                          </div>
                        </div>
                        
                        <!-- Show Get Started button only when form is not visible -->
                        <button 
                          v-if="!showPinSection"
                          @click="togglePinSection"
                          :disabled="isPinDisabled || isLoadingPin"
                          class="w-full bg-gradient-to-r from-purple-500 to-purple-600 text-white py-2.5 px-4 rounded-xl hover:from-purple-600 hover:to-purple-700 transition-all duration-200 text-sm font-medium shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-not-allowed"
                        >
                          {{ isLoadingPin ? 'Updating...' : (isPinDisabled ? 'PIN login not active' : 'Get Started') }}
                        </button>
                        
                        <!-- Pin Form with TOP BORDER LINE -->
                        <div 
                          v-if="showPinSection"
                          class="mt-4 pt-4 border-t border-gray-100"
                        >
                          <div class="space-y-3">
                            <div>
                              <label class="block text-xs font-medium text-gray-700 mb-1">Current Pin</label>
                              <div class="relative flex items-center">
                                <input 
                                  :type="showCurrentPin ? 'text' : 'password'"
                                  v-model="pinForm.current"
                                  maxlength="4"
                                  class="w-full px-3 py-2 pr-10 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent text-center text-lg tracking-widest transition-all duration-200"
                                  placeholder="••••"
                                />
                                <button
                                  type="button"
                                  @click="showCurrentPin = !showCurrentPin"
                                  class="absolute right-3 inset-y-0 my-auto flex items-center justify-center text-gray-400 hover:text-gray-600 transition-colors duration-200 z-10"
                                >
                                  <Eye v-if="!showCurrentPin" class="w-4 h-4" />
                                  <EyeOff v-else class="w-4 h-4" />
                                </button>
                              </div>
                            </div>
                            <div>
                              <label class="block text-xs font-medium text-gray-700 mb-1">New Pin</label>
                              <div class="relative flex items-center">
                                <input 
                                  :type="showNewPin ? 'text' : 'password'"
                                  v-model="pinForm.new"
                                  maxlength="4"
                                  class="w-full px-3 py-2 pr-10 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent text-center text-lg tracking-widest transition-all duration-200"
                                  placeholder="••••"
                                />
                                <button
                                  type="button"
                                  @click="showNewPin = !showNewPin"
                                  class="absolute right-3 inset-y-0 my-auto flex items-center justify-center text-gray-400 hover:text-gray-600 transition-colors duration-200 z-10"
                                >
                                  <Eye v-if="!showNewPin" class="w-4 h-4" />
                                  <EyeOff v-else class="w-4 h-4" />
                                </button>
                              </div>
                            </div>
                            <div>
                              <label class="block text-xs font-medium text-gray-700 mb-1">Confirm Pin</label>
                              <div class="relative flex items-center">
                                <input 
                                  :type="showConfirmPin ? 'text' : 'password'"
                                  v-model="pinForm.confirm"
                                  maxlength="4"
                                  class="w-full px-3 py-2 pr-10 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent text-center text-lg tracking-widest transition-all duration-200"
                                  placeholder="••••"
                                />
                                <button
                                  type="button"
                                  @click="showConfirmPin = !showConfirmPin"
                                  class="absolute right-3 inset-y-0 my-auto flex items-center justify-center text-gray-400 hover:text-gray-600 transition-colors duration-200 z-10"
                                >
                                  <Eye v-if="!showConfirmPin" class="w-4 h-4" />
                                  <EyeOff v-else class="w-4 h-4" />
                                </button>
                              </div>
                            </div>
                          </div>
                          
                          <!-- Buttons Section with spacing -->
                          <div class="space-y-3 mt-4">
                            <!-- Update Pin Button -->
                            <button 
                              @click="changePin"
                              :disabled="isLoadingPin"
                              class="w-full bg-gradient-to-r from-purple-500 to-purple-600 text-white py-2 px-4 rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all duration-200 text-sm font-medium disabled:opacity-70 disabled:cursor-not-allowed"
                            >
                              {{ isLoadingPin ? 'Updating...' : 'Update Pin' }}
                            </button>
                            
                            <!-- Cancel Button -->
                            <button 
                              @click="togglePinSection"
                              class="w-full bg-gradient-to-r from-purple-300 to-purple-400 text-gray-700 font-semibold py-2 px-4 rounded-lg hover:from-purple-400 hover:to-purple-500 transition-all duration-200 text-sm font-medium"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>

                  </div>
                </div>

                <!-- Reset Password/PIN via OTP Card -->
                <div class="mb-8">
                  <div class="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden group">
                    <div class="p-5">
                      <div class="flex items-center mb-4">
                        <div class="w-10 h-10 bg-orange-100 rounded-xl flex items-center justify-center mr-3 group-hover:bg-orange-200 transition-colors duration-200">
                          <KeyRound class="w-5 h-5 text-orange-600" />
                        </div>
                        <div>
                          <h4 class="text-sm font-semibold text-gray-900">Forgot Password/PIN via OTP</h4>
                          <p class="text-xs text-gray-500">Recover your account credentials if forgotten</p>
                        </div>
                      </div>

                      <button
                        v-if="!showResetPasswordSection"
                        @click="toggleResetPasswordSection"
                        :disabled="isLoadingReset"
                        class="w-full bg-gradient-to-r from-orange-500 to-orange-600 text-white py-2.5 px-4 rounded-xl hover:from-orange-600 hover:to-orange-700 transition-all duration-200 text-sm font-medium shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-not-allowed"
                      >
                        {{ isLoadingReset ? 'Loading...' : 'Get Started' }}
                      </button>

                      <div v-if="showResetPasswordSection" class="mt-4 pt-4 border-t border-gray-100">
                        <h3 class="text-sm font-semibold text-[#2B5329] mb-2 text-center">
                          {{ currentResetStep === 1 ? 'Send Verification Code' :
                             currentResetStep === 2 ? 'Verify Code' : 'Create New Credential' }}
                        </h3>
                        <p v-if="currentResetStep === 1" class="text-xs text-gray-600 text-center mb-4">
                          A code will be sent to your registered phone number: <span class="font-bold text-emerald-600">{{ user?.phoneNumber }}</span>
                        </p>

                        <!-- Step 1: Send Code -->
                        <form v-if="currentResetStep === 1" @submit.prevent="handleSendResetCode" class="space-y-4">
                          <button
                            type="submit" :disabled="isLoadingReset"
                            class="w-full py-2.5 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-xl hover:from-orange-600 hover:to-orange-700 transition-all duration-200 text-sm font-medium shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-not-allowed"
                          >
                            {{ isLoadingReset ? "Sending Code..." : "Send Code" }}
                          </button>
                        </form>

                        <!-- Step 2: Verification Code -->
                        <form v-if="currentResetStep === 2" @submit.prevent="handleVerifyCode" class="space-y-6">
                          <div class="text-center">
                            <h3 class="text-sm font-semibold text-[#2B5329] mb-2">Enter the 6-digit code</h3>
                            <p class="text-sm text-gray-600">We sent to your phone number</p>
                          </div>

                          <div class="flex justify-center gap-2">
                            <template v-for="i in 6" :key="i">
                              <input
                                type="text"
                                :ref="el => codeRefs[i-1] = el"
                                v-model="verificationDigits[i-1]"
                                maxlength="1"
                                class="w-12 h-12 text-center text-lg border-2 border-gray-300 rounded-lg focus:border-[#2B5329] focus:ring-2 focus:ring-[#2B5329] focus:outline-none transition-colors"
                                @input="handleCodeInput($event, i-1)"
                                @keydown.delete="handleBackspace($event, i-1)"
                                @keydown.left="focusPrevious(i-1)"
                                @keydown.right="focusNext(i-1)"
                                @paste="handlePaste"
                              />
                            </template>
                          </div>

                          <button
                            type="submit" :disabled="isLoadingReset"
                            class="w-full py-2.5 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-xl hover:from-orange-600 hover:to-orange-700 transition-all duration-200 text-sm font-medium shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-not-allowed"
                          >
                            {{ isLoadingReset ? "Verifying Code..." : "Verify Code" }}
                          </button>

                          <div class="text-center mt-4">
                            <p class="text-sm text-gray-600">
                              Didn't receive the code?
                              <button
                                type="button"
                                @click="handleResendCode"
                                class="text-[#2B5329] hover:text-[#FFA500] font-medium transition-colors ml-1"
                                :disabled="resendTimer > 0"
                              >
                                {{ resendTimer > 0 ? `Resend in ${resendTimer}s` : 'Resend Code' }}
                              </button>
                            </p>
                          </div>
                        </form>

                        <!-- Step 3: New Password / PIN -->
                        <form v-if="currentResetStep === 3" @submit.prevent="handleResetPassword" class="space-y-4">
                          <div class="text-center mb-4">
                            <p class="text-sm text-gray-600">Choose how you'd like to secure your account.</p>
                          </div>

                          <!-- Auth Type Choice -->
                          <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Choose New Login Type</label>
                            <div class="flex gap-2">
                              <button
                                type="button"
                                @click="resetAuthType = 'password'"
                                :class="[
                                  'px-4 py-1.5 rounded-md text-sm font-medium transition w-full',
                                  resetAuthType === 'password'
                                    ? 'bg-[#2B5329] text-white shadow'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                ]"
                              >
                                New Password
                              </button>
                              <button
                                type="button"
                                @click="resetAuthType = 'pin'"
                                :class="[
                                  'px-4 py-1.5 rounded-md text-sm font-medium transition w-full',
                                  resetAuthType === 'pin'
                                    ? 'bg-[#2B5329] text-white shadow'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                ]"
                              >
                                New 4-digit PIN
                              </button>
                            </div>
                          </div>

                          <!-- Password Inputs -->
                          <div v-if="resetAuthType === 'password'" class="space-y-4">
                            <div>
                              <label for="newResetPassword" class="block text-sm font-medium text-gray-700">New Password</label>
                              <div class="relative">
                                <input
                                  :type="showNewResetPassword ? 'text' : 'password'"
                                  id="newResetPassword"
                                  v-model="newResetPassword"
                                  required
                                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329]"
                                />
                                <button type="button" @click="showNewResetPassword = !showNewResetPassword" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                                  <Eye v-if="!showNewResetPassword" class="h-4 w-4" /><EyeOff v-else class="h-4 w-4" />
                                </button>
                              </div>
                            </div>
                            <div>
                              <label for="confirmResetPassword" class="block text-sm font-medium text-gray-700">Confirm Password</label>
                              <div class="relative">
                                <input
                                  :type="showConfirmResetPassword ? 'text' : 'password'"
                                  id="confirmResetPassword"
                                  v-model="confirmResetPassword"
                                  required
                                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329]"
                                />
                                <button type="button" @click="showConfirmResetPassword = !showConfirmResetPassword" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                                  <Eye v-if="!showConfirmResetPassword" class="h-4 w-4" /><EyeOff v-else class="h-4 w-4" />
                                </button>
                              </div>
                            </div>
                          </div>

                          <!-- PIN Inputs -->
                          <div v-else class="space-y-4">
                            <div>
                              <label for="newResetPin" class="block text-sm font-medium text-gray-700">New 4-digit PIN</label>
                              <input id="newResetPin" type="password" v-model="newResetPin" required maxlength="4" pattern="\d*" inputmode="numeric" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329]" />
                            </div>
                            <div>
                              <label for="confirmResetPin" class="block text-sm font-medium text-gray-700">Confirm PIN</label>
                              <input id="confirmResetPin" type="password" v-model="confirmResetPin" required maxlength="4" pattern="\d*" inputmode="numeric" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329]" />
                            </div>
                          </div>

                          <button
                            type="submit" :disabled="isLoadingReset"
                            class="w-full py-2.5 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-xl hover:from-orange-600 hover:to-orange-700 transition-all duration-200 text-sm font-medium shadow-md hover:shadow-lg transform hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-not-allowed"
                          >
                            {{ isLoadingReset ? "Resetting..." : "Reset Credentials" }}
                          </button>
                        </form>
                        <button
                          @click="toggleResetPasswordSection"
                          class="w-full bg-gray-200 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-300 transition-colors duration-200 text-sm font-medium mt-4"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Account Actions Section -->
                <div>
                  <!-- Header with improved icon for 'Account Actions' -->
                  <div class="flex items-center mb-6">
                    <div class="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center mr-4">
                      <UserCog class="w-5 h-5 text-red-600" />
                    </div>
                    <div>
                      <h3 class="text-base font-semibold text-gray-900">Account Actions</h3>
                      <p class="text-sm text-gray-500">Manage your account session</p>
                    </div>
                  </div>

                  <!-- Logout Section -->
                  <div class="bg-white rounded-2xl border border-red-200 shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden">
                    <div class="p-5">
                      <div class="flex items-center justify-between">
                        <div class="flex items-center">
                          <div class="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center mr-3">
                            <LogOut class="w-5 h-5 text-red-600" />
                          </div>
                          <p class="text-sm font-medium text-red-600">Sign out of your account</p>
                        </div>
                        <button 
                          @click="promptLogout"
                          class="bg-gradient-to-r from-red-500 to-red-600 text-white py-2.5 px-8 rounded-xl hover:from-red-600 hover:to-red-700 transition-all duration-200 text-sm font-medium shadow-md hover:shadow-lg transform hover:-translate-y-0.5 min-w-[140px]"
                        >
                          Logout
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    <LogoutModal v-if="showModal" @confirm="executeLogout" @cancel="showModal = false" />

    <!-- Toast Notification - Bottom Right -->
    <div 
      v-if="showToast" 
      class="fixed bottom-4 right-4 bg-white border border-gray-200 rounded-xl shadow-xl p-4 z-50 flex items-center transform transition-all duration-300 ease-in-out backdrop-blur-sm"
    >
      <div class="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center mr-3">
        <CheckCircle class="w-4 h-4 text-emerald-600" />
      </div>
      <span class="text-gray-900 font-medium text-sm">{{ toastMessage }}</span>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../utils/user'
import { 
  User, Phone, Lock, Shield, UserCog,
  LogOut, CheckCircle, Eye, EyeOff,
  KeyRound, Edit3, X
} from 'lucide-vue-next'
import LogoutModal from '../layout/LogoutModal.vue'
import { getDoc, doc, updateDoc, getFirestore, addDoc } from 'firebase/firestore'
import { collection, query, where, getDocs, serverTimestamp } from "firebase/firestore"

const db = getFirestore()
const router = useRouter()
const userStore = useUserStore()

// Use the user from the store
const user = computed(() => userStore.user)
const userId = computed(() => userStore.userId)

// Other existing refs and reactive objects remain the same...
const showToast = ref(false)
const toastMessage = ref('')
const showPasswordSection = ref(false)
const showPinSection = ref(false)
const showModal = ref(false)
const isEditMode = ref(false)
const originalData = ref({})
const hasChanges = ref(false)
const isLoadingProfile = ref(false)
const isLoadingPassword = ref(false)
const isLoadingPin = ref(false)
const isLoadingReset = ref(false)

const showToastMessage = (message, severity = 'info', persistKey = null) => {
  window.showToast(message, severity)
}

// Initialize profileData with store data
const profileData = reactive({
  name: '',
  phone: ''
})

// Other existing computed properties and methods remain the same...
const isPasswordDisabled = computed(() => userStore.user?.authType === 'pin')
const isPinDisabled = computed(() => userStore.user?.authType === 'password')

const canSave = computed(() => {
  return isEditMode.value && hasChanges.value
})

// Avatar options...
const avatarOptions = ref([
  { id: 1, icon: '🌱', name: 'Seedling' },
  { id: 2, icon: '🌿', name: 'Herb' },
  { id: 3, icon: '🌾', name: 'Wheat' },
  { id: 4, icon: '🌽', name: 'Corn' },
  { id: 5, icon: '🥕', name: 'Carrot' },
  { id: 6, icon: '🍅', name: 'Tomato' },
  { id: 7, icon: '🥬', name: 'Lettuce' },
  { id: 8, icon: '🌻', name: 'Sunflower' },
  { id: 9, icon: '🌳', name: 'Tree' },
  { id: 10, icon: '🍃', name: 'Leaves' },
  { id: 11, icon: '🌵', name: 'Cactus' },
  { id: 12, icon: '🌸', name: 'Blossom' },
  { id: 13, icon: '🍄', name: 'Mushroom' },
  { id: 14, icon: '🌺', name: 'Hibiscus' },
  { id: 15, icon: '🌹', name: 'Rose' },
  { id: 16, icon: '🌷', name: 'Tulip' },
  { id: 17, icon: '🥦', name: 'Broccoli' },
  { id: 18, icon: '🌶️', name: 'Pepper' },
  { id: 19, icon: '🥒', name: 'Cucumber' },
  { id: 20, icon: '🍆', name: 'Eggplant' },
  { id: 21, icon: '🥔', name: 'Potato' },
  { id: 22, icon: '🧄', name: 'Garlic' },
  { id: 23, icon: '🧅', name: 'Onion' },
  { id: 24, icon: '🥜', name: 'Peanut' }
])

const selectedAvatar = ref(avatarOptions.value[0])

// Password and PIN forms...
const passwordForm = reactive({
  current: '',
  new: '',
  confirm: ''
})

const pinForm = reactive({
  current: '',
  new: '',
  confirm: ''
})

// Watch for user changes and update profileData
watch(() => userStore.user, (newUser) => {
  if (newUser) {
    profileData.name = newUser.name || ''
    profileData.phone = newUser.phoneNumber || ''
    originalData.value = {
      name: profileData.name,
      phone: profileData.phone
    }
    
    // Set selected avatar
    if (newUser.avatar) {
      selectedAvatar.value = avatarOptions.value.find(
        opt => opt.id === newUser.avatar.id
      ) || avatarOptions.value[0]
    }
  }
}, { immediate: true })


// Edit mode functions
const toggleEditMode = () => {
  if (isEditMode.value) {
    // Cancel editing - restore original data
    profileData.name = originalData.value.name
    profileData.phone = originalData.value.phone
    hasChanges.value = false
  } else {
    // Start editing - save current data as original
    originalData.value = {
      name: profileData.name,
      phone: profileData.phone
    }
  }
  isEditMode.value = !isEditMode.value
}

const onFieldChange = () => {
  if (!isEditMode.value) return
  
  hasChanges.value = (
    profileData.name !== originalData.value.name ||
    profileData.phone !== originalData.value.phone
  )
}

// Add this utility function at the top of your script
const normalizePhoneNumber = (phone) => {
  if (!phone) return null;
  
  // Remove all non-digit characters
  let normalized = phone.replace(/\D/g, '');
  
  // Handle Philippine numbers specifically
  if (normalized.startsWith('0')) {
    normalized = '+63' + normalized.substring(1);
  } else if (normalized.startsWith('63')) {
    normalized = '+' + normalized;
  } else if (!normalized.startsWith('+')) {
    normalized = '+63' + normalized;
  }
  
  return normalized;
};

// Update saveProfile to use the store properly
const saveProfile = async () => {
  if (!canSave.value) return;
  
  isLoadingProfile.value = true;

  // Get current values
  const name = profileData.name?.trim() || '';
  const phone = profileData.phone?.trim() || '';

  if (!name) {
    showToastMessage('Name is required');
    isLoadingProfile.value = false;
    return;
  }

  if (!phone) {
    showToastMessage('Phone number is required');
    isLoadingProfile.value = false;
    return;
  }

  try {
    // 1. First query for the user document by phone number
    const usersRef = collection(db, 'users');
    const q = query(usersRef, where('phoneNumber', '==', phone));
    const querySnapshot = await getDocs(q);

    if (querySnapshot.empty) {
      throw new Error('User document not found');
    }

    // 2. Get the first matching document (assuming phone numbers are unique)
    const userDoc = querySnapshot.docs[0];
    
    // 3. Update the document with its actual ID
    await updateDoc(doc(db, 'users', userDoc.id), {
      name: name,
      phoneNumber: phone,
      avatar: selectedAvatar.value,
      updatedAt: serverTimestamp()
    });

    // 4. Update local state
    const updatedUser = {
      ...userStore.user,
      name: name,
      phoneNumber: phone,
      avatar: selectedAvatar.value
    };

    userStore.setUser(updatedUser);
    localStorage.setItem('user', JSON.stringify({
      user: updatedUser,
      userId: userDoc.id  // Store the actual document ID
    }));

    // 5. Reset edit mode
    originalData.value = { name, phone };
    hasChanges.value = false;
    isEditMode.value = false;
    
    showToastMessage('Profile updated successfully!');
  } catch (err) {
    console.error('Update error:', err);
    
    if (err.message.includes('not found')) {
      showToastMessage('User record not found in database');
    } else {
      showToastMessage('Failed to update profile. Please try again.');
    }
  } finally {
    isLoadingProfile.value = false;
  }
}

const selectAvatar = async (avatar) => {
  selectedAvatar.value = avatar;
  showToastMessage(`Avatar changed to ${avatar.name}`);

  // Get the user ID - try multiple sources
  const currentUserId = userId.value || 
                      userStore.userId || 
                      userStore.user?.id || 
                      JSON.parse(localStorage.getItem('user'))?.userId;

  if (!currentUserId) {
    console.error('User ID not found in any source');
    showToastMessage('Please login again');
    return;
  }

  try {
    await updateDoc(doc(db, 'users', currentUserId), {
      avatar: avatar,
      updatedAt: serverTimestamp()
    });

    // Update local state - maintain all existing user data
    const updatedUser = {
      ...userStore.user,
      avatar: avatar
    };
    
    // Update store
    userStore.setUser(updatedUser);
    
    // Update localStorage - maintain the same structure
    localStorage.setItem('user', JSON.stringify({
      user: updatedUser,
      userId: currentUserId
    }));

    showToastMessage('Avatar updated successfully!');
  } catch (error) {
    console.error('Firestore update error:', error);
    showToastMessage('Failed to save avatar. Please try again.');
    
    // Revert UI on error
    selectedAvatar.value = userStore.user?.avatar || avatarOptions.value[0];
  }
}

const changePassword = async () => {
  isLoadingPassword.value = true
  const uid = localStorage.getItem('uid')

  if (!uid || user.value?.user?.authType !== 'password') return

  if (
    !passwordForm.current ||
    !passwordForm.new ||
    !passwordForm.confirm ||
    passwordForm.new !== passwordForm.confirm
  ) {
    showToastMessage('Please fill and confirm password fields correctly')
    isLoadingPassword.value = false
    return
  }

  if (passwordForm.new.length < 6) {
    showToastMessage('Password must be at least 6 characters')
    isLoadingPassword.value = false
    return
  }

  try {
    if (user.value?.user?.password !== passwordForm.current) {
      showToastMessage('Current password is incorrect')
      isLoadingPassword.value = false
      return
    }

    await updateDoc(doc(db, 'users', uid), {
      password: passwordForm.new
    })

    // Update local user data
    const updatedUser = {
      ...user.value,
      user: {
        ...user.value.user,
        password: passwordForm.new
      }
    }

    localStorage.setItem('user', JSON.stringify(updatedUser))
    sessionStorage.setItem('user', JSON.stringify(updatedUser))
    userStore.setUser(updatedUser)

    passwordForm.current = ''
    passwordForm.new = ''
    passwordForm.confirm = ''
    showToastMessage('Password updated successfully!')
  } catch (err) {
    console.error('Error updating password:', err)
    showToastMessage('Failed to update password.')
  } finally {
    isLoadingPassword.value = false
  }
}

const changePin = async () => {
  isLoadingPin.value = true
  const uid = localStorage.getItem('uid')

  if (!uid || user.value?.user?.authType !== 'pin') return

  if (
    !pinForm.current ||
    !pinForm.new ||
    !pinForm.confirm ||
    pinForm.new !== pinForm.confirm ||
    pinForm.new.length !== 4
  ) {
    showToastMessage('Please enter and confirm a valid 4-digit PIN.')
    isLoadingPin.value = false
    return
  }

  try {
    if (user.value?.user?.pin !== pinForm.current) {
      showToastMessage('Current PIN is incorrect')
      isLoadingPin.value = false
      return
    }

    await updateDoc(doc(db, 'users', uid), {
      pin: pinForm.new
    })

    // Update local user data
    const updatedUser = {
      ...user.value,
      user: {
        ...user.value.user,
        pin: pinForm.new
      }
    }

    localStorage.setItem('user', JSON.stringify(updatedUser))
    sessionStorage.setItem('user', JSON.stringify(updatedUser))
    userStore.setUser(updatedUser)

    pinForm.current = ''
    pinForm.new = ''
    pinForm.confirm = ''
    showToastMessage('PIN updated successfully!')
  } catch (err) {
    console.error('Error updating PIN:', err)
    showToastMessage('Failed to update PIN.')
  } finally {
    isLoadingPin.value = false
  }
}

// Utility functions for phone number validation
function isValidPhilippinePhoneNumber(number) {
  const cleaned = number.trim();
  return /^(\+639|09)\d{9}$/.test(cleaned);
}

function toE164(phone) {
  const trimmed = phone.trim();
  if (trimmed.startsWith('+63')) return trimmed;
  const cleaned = trimmed.replace(/\D/g, '');
  if (cleaned.startsWith('0')) return '+63' + cleaned.slice(1);
  if (cleaned.startsWith('63')) return '+' + cleaned;
  return null;
}

// OTP input handlers
const handleCodeInput = (event, index) => {
  const value = event.target.value
  if (!/^\d*$/.test(value)) {
    verificationDigits.value[index] = ''
    return
  }
  if (value && index < 5) {
    codeRefs.value[index + 1]?.focus()
  }
}

const handleBackspace = (event, index) => {
  if (!verificationDigits.value[index] && index > 0) {
    codeRefs.value[index - 1]?.focus()
  }
}

const focusPrevious = (index) => {
  if (index > 0) {
    codeRefs.value[index - 1]?.focus()
  }
}

const focusNext = (index) => {
  if (index < 5) {
    codeRefs.value[index + 1]?.focus()
  }
}

const handlePaste = (event) => {
  event.preventDefault()
  const pastedData = event.clipboardData.getData('text')
  const numbers = pastedData.match(/\d/g)
  if (numbers) {
    numbers.slice(0, 6).forEach((num, i) => {
      verificationDigits.value[i] = num
    })
  }
}

// Resend timer logic
let resendInterval = null
const startResendTimer = () => {
  resendTimer.value = 30
  resendInterval = setInterval(() => {
    if (resendTimer.value > 0) {
      resendTimer.value--
    } else {
      clearInterval(resendInterval)
    }
  }, 1000)
}

// Reset Password/PIN flow functions
const handleSendResetCode = async () => {
  const trimmedPhone = user.value?.phoneNumber?.trim()
  if (!isValidPhilippinePhoneNumber(trimmedPhone)) {
    showToastMessage('Invalid phone number. Please update your profile first.')
    return
  }

  const formattedPhone = toE164(trimmedPhone)
  if (!formattedPhone) {
    showToastMessage('Could not format phone number.')
    return
  }

  isLoadingReset.value = true;

  try {
    const usersRef = collection(db, 'users');
    const q = query(usersRef, where('phoneNumber', '==', formattedPhone));
    const snapshot = await getDocs(q);

    if (snapshot.empty) {
      showToastMessage('This phone number is not registered yet.');
      isLoadingReset.value = false;
      return;
    }

    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    const userDoc = snapshot.docs[0];

    await updateDoc(doc(db, 'users', userDoc.id), {
      otp,
      otpSentAt: serverTimestamp()
    });

    // Note: You'll need to implement the API call for sending SMS
    // await api.post('/otp/send', {
    //   number: formattedPhone,
    //   message: `Your password reset code is: ${otp}`
    // });

    showToastMessage('A password reset code has been sent to your phone.');
    currentResetStep.value = 2;
    startResendTimer();

  } catch (error) {
    console.error("Error sending reset code:", error);
    showToastMessage("Error sending reset code.");
  } finally {
    isLoadingReset.value = false;
  }
};

const handleResendCode = async () => {
  if (resendTimer.value > 0) return;
  isLoadingReset.value = true;
  try {
    const trimmedPhone = user.value?.phoneNumber?.trim()
    const formattedPhone = toE164(trimmedPhone)

    const usersRef = collection(db, 'users');
    const q = query(usersRef, where('phoneNumber', '==', formattedPhone));
    const snapshot = await getDocs(q);
    const userDoc = snapshot.docs[0];

    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    await updateDoc(doc(db, 'users', userDoc.id), { otp, otpSentAt: serverTimestamp() });

    // await api.post('/otp/send', { number: formattedPhone, message: `Your new password reset code is: ${otp}` });

    showToastMessage("A new code has been sent to your phone.");
    startResendTimer();

  } catch (error) {
    console.error("Error resending code:", error);
    showToastMessage("Error resending code.");
  } finally {
    isLoadingReset.value = false;
  }
}

const handleVerifyCode = async () => {
  const code = verificationDigits.value.join('').trim();

  if (code.length !== 6) {
    showToastMessage('Please enter the 6-digit code.');
    return;
  }

  isLoadingReset.value = true;

  try {
    const formattedPhone = toE164(user.value?.phoneNumber);
    const q = query(collection(db, 'users'), where('phoneNumber', '==', formattedPhone));
    const querySnapshot = await getDocs(q);

    if (querySnapshot.empty) {
      showToastMessage('User not found. Please start over.');
      currentResetStep.value = 1;
      return;
    }

    const userDoc = querySnapshot.docs[0];
    const userData = userDoc.data();

    if (userData.otp !== code) {
      showToastMessage('Invalid verification code.');
      return;
    }

    await updateDoc(doc(db, 'users', userDoc.id), {
      otp: '',
    });

    showToastMessage('Code verified successfully!');
    currentResetStep.value = 3;

  } catch (error) {
    console.error('Error verifying code:', error);
    showToastMessage('An error occurred during verification.');
  } finally {
    isLoadingReset.value = false;
  }
}

const handleResetPassword = async () => {
  isLoadingReset.value = true;

  const formattedPhone = toE164(user.value?.phoneNumber);
  if (!formattedPhone) {
    showToastMessage('Invalid phone number format.');
    isLoadingReset.value = false;
    return;
  }

  const updateData = {
    authType: resetAuthType.value,
    updatedAt: serverTimestamp()
  };

  if (resetAuthType.value === 'password') {
    if (newResetPassword.value !== confirmResetPassword.value) {
      showToastMessage('Passwords do not match!');
      isLoadingReset.value = false;
      return;
    }
    if (newResetPassword.value.length < 6) {
      showToastMessage('Password must be at least 6 characters long.');
      isLoadingReset.value = false;
      return;
    }
    updateData.password = newResetPassword.value;
    updateData.pin = '';
  } else {
    if (newResetPin.value !== confirmResetPin.value) {
      showToastMessage('PINs do not match!');
      isLoadingReset.value = false;
      return;
    }
    if (!/^\d{4}$/.test(newResetPin.value)) {
        showToastMessage('PIN must be 4 digits.');
        isLoadingReset.value = false;
        return;
    }
    updateData.pin = newResetPin.value;
    updateData.password = '';
  }

  try {
    const usersRef = collection(db, 'users');
    const q = query(usersRef, where('phoneNumber', '==', formattedPhone));
    const snapshot = await getDocs(q);

    if (snapshot.empty) {
      showToastMessage('Could not find an account with that phone number.');
      isLoadingReset.value = false;
      return;
    }

    const userDocRef = snapshot.docs[0].ref;
    await updateDoc(userDocRef, updateData);

    const updatedUser = { ...user.value, ...updateData };
    localStorage.setItem('user', JSON.stringify(updatedUser));
    sessionStorage.setItem('user', JSON.stringify(updatedUser));
    user.value = updatedUser;

    showToastMessage('Your credentials have been reset successfully.');
    toggleResetPasswordSection();
    currentResetStep.value = 1;
    newResetPassword.value = '';
    confirmResetPassword.value = '';
    newResetPin.value = '';
    confirmResetPin.value = '';

  } catch (error) {
    console.error("Error resetting password:", error);
    showToastMessage("An error occurred while resetting your credentials.");
  } finally {
    isLoadingReset.value = false;
  }
};

const promptLogout = () => {
  showModal.value = true;
}

const executeLogout = () => {
  userStore.logout()
}

onMounted(async () => {
  // Load user if not already loaded
  if (!userStore.isAuthenticated) {
    await userStore.loadUser()
  }

  // Set initial avatar
  if (userStore.user?.avatar) {
    selectedAvatar.value = avatarOptions.value.find(
      opt => opt.id === userStore.user.avatar.id
    ) || avatarOptions.value[0]
  }

  // Set auth type visibility
  if (userStore.user?.authType === 'pin') {
    showPasswordSection.value = false
  } else if (userStore.user?.authType === 'password') {
    showPinSection.value = false
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

::-webkit-scrollbar {
  width: 4px;
}

::-webkit-scrollbar-track {
  background: transparent;
  margin: 8px 0;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

* {
  transition: all 200ms ease-in-out;
}

input:focus {
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

button:hover {
  transform: translateY(-1px);
}

button:active {
  transform: translateY(0);
}

@media (max-width: 1024px) {
  .w-\[30\%\] {
    width: 35%;
  }
  
  .grid-cols-1.md\\:grid-cols-2 {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .flex.gap-6 {
    flex-direction: column;
    gap: 1rem;
  }
  
  .w-\[30\%\] {
    width: 100%;
    min-height: 300px;
  }
  
  .grid-cols-5 {
    grid-template-columns: repeat(6, 1fr);
  }
  
  .w-32.h-32 {
    width: 5rem;
    height: 5rem;
  }
  
  .px-3 {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
}

@media (max-width: 640px) {
  .p-6 {
    padding: 1rem;
  }
  
  .px-3 {
    padding-left: 0.25rem;
    padding-right: 0.25rem;
  }
  
  .gap-4 {
    gap: 0.375rem;
  }
}

@media (max-width: 480px) {
  .grid-cols-5 {
    grid-template-columns: repeat(5, 1fr);
  }
  
  .w-14.h-14 {
    width: 2.25rem;
    height: 2.25rem;
  }
}
</style>