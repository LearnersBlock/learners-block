module.exports = {
    root: true,
    env: {
        node: true,
        browser: true
    },
    extends: [
        'plugin:vue/essential',
        // 'eslint:recommended',
        'standard'
    ],
    parserOptions: {
        parser: 'babel-eslint'
    },
    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
        'generator-star-spacing': 'off',
        // update ESLint and remove rule line 21 + 24
        // https://github.com/babel/babel-eslint/issues/530
        'template-curly-spacing': 'off',
        indent: [
            'error', 4,
            { ignoredNodes: ['TemplateLiteral'] }
        ]
    }
}
