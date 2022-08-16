<script lang="ts" setup>

import { useAuth0 } from '@auth0/auth0-vue';
import { backend } from "../env.json";
import { ref } from 'vue';

const { getAccessTokenSilently, loginWithPopup, loginWithRedirect, user, isAuthenticated } = useAuth0();
let message = ref<null | string>(null);

async function postRequestPrivateAPI() {
    const response = await fetch(`${backend}/api/private`, {
        headers: {
            Authorization: 'Bearer ' + token.value
        }
    });
    message.value = await response.json();
}

const token = ref<null | string>(null);

async function setTokenSilently() {
    token.value = await getAccessTokenSilently();
}

function redirectToBackendLogin() {
    location.replace(`${backend}/login`);
}

</script>

<template>
    <div>
        <h2 v-if="isAuthenticated">Authenticated</h2>
        <h2 v-else>Not Authenticated</h2>
        <code>{{ user }}</code>
    </div>
    <div>
        <h2>use if not authenticated</h2>
        <button @click="loginWithRedirect">implicit loginWithRedirect</button>
        <button @click="loginWithPopup">implicit loginWithPopup</button>
        <button @click="redirectToBackendLogin">Authorization Code Flow login</button>
    </div>
    <div>
        <h2 v-if="token">Token</h2>
        <h2 v-else>No Token</h2>
        <code>{{ token }}</code>
    </div>
    <div>
        <button @click="postRequestPrivateAPI" v-if="token">if token found, post request private API</button>
        <button @click="setTokenSilently" v-else-if="1">if logged in once, getAccessTokenSilently</button>
    </div>
    <div v-if="message">
        <h2>Message</h2>
        <code>{{ message }}</code>
    </div>
</template>

<style scoped>

button {
    margin: .5rem;
}

</style>