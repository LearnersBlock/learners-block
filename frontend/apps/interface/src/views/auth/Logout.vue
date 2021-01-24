<template>
    <AuthLogout :title="$t('auth-screen.logout.title')" />
</template>

<script>
import AuthLogout from '@/components/Auth/AuthLogout'

export default {
    name: 'Logout',
    components: {
        AuthLogout
    }
}
</script>
