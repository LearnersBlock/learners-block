<template>
    <AuthLogin
        :title="$t('auth-screen.login.title')"
        :description="$t('auth-screen.login.description')">
    </AuthLogin>
</template>

<script>
import AuthLogin from '@/components/Auth/AuthLogin'

export default {
    name: 'Login',
    components: {
        AuthLogin
    }
}
</script>
