require 'rake'

desc "install the dot files into user's home directory"
task :install do
  Dir['*'].each do |file|
    system %Q{ln -vs "#{file}" "$HOME/.#{file}"} unless %w[Rakefile README].include? file
  end
end
